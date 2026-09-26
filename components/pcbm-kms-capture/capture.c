// SPDX-License-Identifier: GPL-2.0-only
/* Project CBM contributors, 2026. See upstream/ for Paul Cercueil's reference. */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <grp.h>
#include <pwd.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/capability.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/sysmacros.h>
#include <linux/dma-buf.h>
#include <drm_fourcc.h>
#include <xf86drm.h>
#include <xf86drmMode.h>
#include <png.h>
#include "policy.h"
#define LIMIT (64u*1024u*1024u)
/* Stable exit classes, no private diagnostics or DRM identities. */
enum { UNAVAILABLE=20, UNSUPPORTED=21, DENIED=22, FAILED=23, CHANGED=24 };
struct frame { uint32_t connector, plane, crtc, fb, width, height, format, pitch, offset; drmModeModeInfo mode; size_t size; };
static int trusted(int fd, int directory) {
    struct stat s;
    return fstat(fd,&s)==0 && s.st_uid==0 && !(s.st_mode&022) &&
        (directory ? S_ISDIR(s.st_mode) : S_ISREG(s.st_mode));
}
static int authorize(void) {
    const char *u=getenv("SUDO_UID"), *g=getenv("SUDO_GID");
    struct passwd *pw=getpwnam("pcbm");
    if(geteuid()!=0 || !u || strcmp(u,"1000") || !g || strcmp(g,"1000") ||
       !pw || pw->pw_uid!=1000 || pw->pw_gid!=1000 || strcmp(pw->pw_dir,"/home/pcbm")) return 0;
    int d=open("/",O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC);
    const char *parts[]={"etc","project-cbm","configuration-policy.json"};
    if(d<0 || !trusted(d,1)) { if(d>=0)close(d); return 0; }
    for(unsigned i=0;i<3;i++) {
        int n=openat(d,parts[i],O_RDONLY|O_CLOEXEC|O_NOFOLLOW|(i<2?O_DIRECTORY:0));
        close(d); d=n;
        if(d<0 || !trusted(d,i<2)) { if(d>=0)close(d); return 0; }
    }
    char buf[4097]; ssize_t n=read(d,buf,sizeof(buf)); close(d);
    if(n<1 || n>=4096 || memchr(buf,0,(size_t)n)) return 0;
    buf[n]=0; return ready_policy(buf);
}
static int drop(void) {
    /* Bounding and ambient sets cannot survive as latent regain paths. */
    for(int i=0;i<=CAP_LAST_CAP;i++) if(prctl(PR_CAPBSET_DROP,i,0,0,0)) return 0;
    if(prctl(PR_CAP_AMBIENT,PR_CAP_AMBIENT_CLEAR_ALL,0,0,0) ||
       prctl(PR_SET_KEEPCAPS,0,0,0,0) || setgroups(0,NULL) ||
       setresgid(1000,1000,1000) || setresuid(1000,1000,1000)) return 0;
    cap_t empty=cap_init(); if(!empty) return 0;
    int rc=cap_set_proc(empty); cap_free(empty);
    if(rc || prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0) || prctl(PR_SET_DUMPABLE,0)) return 0;
    uid_t r,e,s; gid_t gr,ge,gs;
    if(getresuid(&r,&e,&s)||getresgid(&gr,&ge,&gs)||r!=1000||e!=1000||s!=1000||
       gr!=1000||ge!=1000||gs!=1000||getgroups(0,NULL)!=0) return 0;
    cap_t caps=cap_get_proc(); if(!caps)return 0;
    int good=1;
    for(int i=0;i<=CAP_LAST_CAP;i++) for(int k=CAP_EFFECTIVE;k<=CAP_INHERITABLE;k++) {
        cap_flag_value_t v;
        if(cap_get_flag(caps,i,(cap_flag_t)k,&v)||v!=CAP_CLEAR)good=0;
    }
    cap_free(caps);
    return good && setuid(0)==-1;
}
static int property(int fd,uint32_t obj,uint32_t type,const char *name,uint64_t *value) {
    drmModeObjectProperties *p=drmModeObjectGetProperties(fd,obj,type);
    if(!p)return -1;
    int found=0;
    for(uint32_t i=0;i<p->count_props;i++) {
        drmModePropertyRes *r=drmModeGetProperty(fd,p->props[i]);
        if(!r) {found=-1;break;}
        if(!strcmp(r->name,name)) { *value=p->prop_values[i];found=1; }
        drmModeFreeProperty(r);
    }
    drmModeFreeObjectProperties(p);return found;
}
static int equals(int fd,uint32_t obj,uint32_t type,const char *name,uint64_t expected,int required) {
    uint64_t value=0; int found=property(fd,obj,type,name,&value);
    return found>=0 && (found ? value==expected : !required);
}
static int describe(int fd,struct frame *f) {
    drmModeRes *r=drmModeGetResources(fd); if(!r)return FAILED;
    unsigned active=0; uint32_t connector=0,crtc=0,w=0,h=0; drmModeModeInfo mode={0};
    int error=0;
    for(int i=0;i<r->count_connectors;i++) {
        drmModeConnector *c=drmModeGetConnectorCurrent(fd,r->connectors[i]);
        if(!c) {error=CHANGED;break;}
        if(c->connection==DRM_MODE_CONNECTED && c->encoder_id) {
            drmModeEncoder *e=drmModeGetEncoder(fd,c->encoder_id);
            if(!e)error=CHANGED;
            else if(e->crtc_id) {
                drmModeCrtc *v=drmModeGetCrtc(fd,e->crtc_id);
                if(!v)error=CHANGED;
                else if(v->mode_valid) {active++;connector=c->connector_id;crtc=e->crtc_id;mode=v->mode;w=mode.hdisplay;h=mode.vdisplay;}
                if(v)drmModeFreeCrtc(v);
            }
            if(e)drmModeFreeEncoder(e);
        }
        drmModeFreeConnector(c);
    }
    drmModeFreeResources(r);
    if(error)return error;
    if(!active)return UNAVAILABLE;
    if(active!=1 || !w || !h || w>4096 || h>4096)return UNSUPPORTED;
    if(!equals(fd,crtc,DRM_MODE_OBJECT_CRTC,"ACTIVE",1,1) ||
       !equals(fd,crtc,DRM_MODE_OBJECT_CRTC,"CTM",0,0) ||
       !equals(fd,crtc,DRM_MODE_OBJECT_CRTC,"GAMMA_LUT",0,0) ||
       !equals(fd,crtc,DRM_MODE_OBJECT_CRTC,"DEGAMMA_LUT",0,0))return UNSUPPORTED;
    drmModePlaneRes *planes=drmModeGetPlaneResources(fd); if(!planes)return FAILED;
    unsigned count=0; struct frame out={0};
    for(uint32_t i=0;i<planes->count_planes;i++) {
        drmModePlane *p=drmModeGetPlane(fd,planes->planes[i]);
        if(!p) {error=CHANGED;break;}
        if(p->fb_id && p->crtc_id) {
            count++; out=(struct frame){.connector=connector,.plane=p->plane_id,.crtc=p->crtc_id,.fb=p->fb_id,.width=w,.height=h,.mode=mode};
        }
        drmModeFreePlane(p);
    }
    drmModeFreePlaneResources(planes);
    if(error)return error;
    if(count!=1 || out.crtc!=crtc)return UNSUPPORTED;
    const char *names[]={"CRTC_X","CRTC_Y","CRTC_W","CRTC_H","SRC_X","SRC_Y","SRC_W","SRC_H","rotation","alpha"};
    uint64_t values[]={0,0,w,h,0,0,(uint64_t)w<<16,(uint64_t)h<<16,DRM_MODE_ROTATE_0,65535};
    for(unsigned i=0;i<10;i++) if(!equals(fd,out.plane,DRM_MODE_OBJECT_PLANE,names[i],values[i],i<8))return UNSUPPORTED;
    *f=out;return 0;
}
static int same(const struct frame *a,const struct frame *b) {
    /* Page flips change framebuffer identity, not display configuration. The
     * exported DMA-BUF pinned the sampled scanout until its read-only copy was
     * complete. Reject mode/layout changes, but do not demand a stopped game. */
    return a->connector==b->connector && a->plane==b->plane && a->crtc==b->crtc &&
        a->width==b->width && a->height==b->height && a->format==b->format &&
        a->pitch==b->pitch && a->offset==b->offset && a->size==b->size &&
        a->mode.clock==b->mode.clock && a->mode.hdisplay==b->mode.hdisplay &&
        a->mode.hsync_start==b->mode.hsync_start && a->mode.hsync_end==b->mode.hsync_end &&
        a->mode.htotal==b->mode.htotal && a->mode.hskew==b->mode.hskew &&
        a->mode.vdisplay==b->mode.vdisplay && a->mode.vsync_start==b->mode.vsync_start &&
        a->mode.vsync_end==b->mode.vsync_end && a->mode.vtotal==b->mode.vtotal &&
        a->mode.vscan==b->mode.vscan && a->mode.flags==b->mode.flags;
}
static void free_fb(int fd,drmModeFB2 *f) {
    if(!f)return;
    for(unsigned i=0;i<4;i++) {
        if(!f->handles[i])continue;
        unsigned j;for(j=0;j<i;j++)if(f->handles[j]==f->handles[i])break;
        if(j==i)drmCloseBufferHandle(fd,f->handles[i]);
    }
    drmModeFreeFB2(f);
}
static int layout(drmModeFB2 *b,struct frame *f) {
    unsigned bytes=b->pixel_format==DRM_FORMAT_RGB565?2:4;
    if(b->width!=f->width || b->height!=f->height ||
       (b->pixel_format!=DRM_FORMAT_RGB565 && b->pixel_format!=DRM_FORMAT_XRGB8888 && b->pixel_format!=DRM_FORMAT_ARGB8888) ||
       b->modifier!=DRM_FORMAT_MOD_LINEAR || (b->flags & ~DRM_MODE_FB_MODIFIERS) || !b->handles[0] || b->pitches[0] < b->width*bytes) return UNSUPPORTED;
    for(unsigned i=1;i<4;i++)if(b->handles[i]||b->pitches[i]||b->offsets[i])return UNSUPPORTED;
    uint64_t size=(uint64_t)b->offsets[0]+(uint64_t)b->pitches[0]*b->height;
    if(size>LIMIT)return UNSUPPORTED;
    f->format=b->pixel_format;f->pitch=b->pitches[0];f->offset=b->offsets[0];f->size=size;return 0;
}
static int pixels(int fd,struct frame *f,unsigned char **output) {
    int rc=CHANGED;
    for(unsigned retry=0;retry<3;retry++) {
        rc=describe(fd,f);if(rc)return rc;
        drmModeFB2 *b=drmModeGetFB2(fd,f->fb);
        if(!b) {rc=CHANGED;continue;}
        if(!b->handles[0]) {free_fb(fd,b);return DENIED;}
        rc=layout(b,f); if(rc) {free_fb(fd,b);return rc;}
        int prime=-1;
        rc=drmPrimeHandleToFD(fd,b->handles[0],DRM_CLOEXEC,&prime);
        free_fb(fd,b);
        if(rc || prime<0)return DENIED;
        off_t size=lseek(prime,0,SEEK_END);
        if(size<0 || (uint64_t)size<f->size) {close(prime);return UNSUPPORTED;}
        struct dma_buf_sync sync={.flags=DMA_BUF_SYNC_START|DMA_BUF_SYNC_READ};
        if(ioctl(prime,DMA_BUF_IOCTL_SYNC,&sync)) {close(prime);return FAILED;}
        void *map=mmap(NULL,f->size,PROT_READ,MAP_SHARED,prime,0);
        unsigned char *copy=NULL;
        if(map!=MAP_FAILED) {
            copy=malloc(f->size);
            if(copy)memcpy(copy,map,f->size);
            munmap(map,f->size);
        }
        sync.flags=DMA_BUF_SYNC_END|DMA_BUF_SYNC_READ;
        int ended=ioctl(prime,DMA_BUF_IOCTL_SYNC,&sync);close(prime);
        if(!copy || ended) {free(copy);return FAILED;}
        struct frame after;
        rc=describe(fd,&after);
        if(!rc) {
            drmModeFB2 *next=drmModeGetFB2(fd,after.fb);
            if(!next)rc=CHANGED;
            else { rc=layout(next,&after);free_fb(fd,next); }
        }
        if(!rc && same(f,&after)) { *output=copy;return 0; }
        free(copy);
        if(rc && rc!=CHANGED && rc!=UNAVAILABLE)return rc;
        rc=CHANGED;
    }
    return rc;
}
static int capture(struct frame *f,unsigned char **pixels_out) {
    drmDevicePtr devices[64]; int count=drmGetDevices2(0,devices,64);
    if(count<0)return UNAVAILABLE;
    if(count>=64) {drmFreeDevices(devices,64);return UNSUPPORTED;}
    int chosen=-1,rc=UNAVAILABLE;
    for(int i=0;i<count;i++) {
        if(!(devices[i]->available_nodes&(1<<DRM_NODE_PRIMARY)))continue;
        const char *path=devices[i]->nodes[DRM_NODE_PRIMARY];
        if(strncmp(path,"/dev/dri/card",13)) {rc=UNSUPPORTED;break;}
        int fd=open(path,O_RDONLY|O_CLOEXEC|O_NOFOLLOW);
        if(fd<0) {rc=DENIED;break;}
        struct stat s;
        if(fstat(fd,&s)||!S_ISCHR(s.st_mode)||major(s.st_rdev)!=226) {close(fd);rc=DENIED;break;}
        /* Opening an idle console node may implicitly assign master. Relinquish
         * immediately; CAP_SYS_ADMIN is sufficient for foreign FB handles. */
        if(drmIsMaster(fd) && drmDropMaster(fd)) {close(fd);rc=DENIED;break;}
        drmVersionPtr v=drmGetVersion(fd);
        int vc4=v && v->name_len==3 && !memcmp(v->name,"vc4",3);
        if(v)drmFreeVersion(v);
        if(!vc4) {close(fd);continue;}
        if(drmSetClientCap(fd,DRM_CLIENT_CAP_ATOMIC,1) || drmSetClientCap(fd,DRM_CLIENT_CAP_UNIVERSAL_PLANES,1)) {close(fd);rc=UNSUPPORTED;break;}
        struct frame candidate;
        int status=describe(fd,&candidate);
        if(status==UNAVAILABLE) {close(fd);continue;}
        if(status || chosen>=0) {close(fd);rc=status?status:UNSUPPORTED;break;}
        chosen=fd;*f=candidate;rc=0;
    }
    drmFreeDevices(devices,count);
    if(!rc && chosen>=0)rc=pixels(chosen,f,pixels_out);
    if(chosen>=0)close(chosen);
    return rc;
}
static void png_error_quiet(png_structp p,const char *message) { (void)message;png_longjmp(p,1); }
static void png_warning_quiet(png_structp p,const char *message) { (void)p;(void)message; }
static int encode(const struct frame *f,const unsigned char *data) {
    unsigned char *row=malloc((size_t)f->width*3);if(!row)return FAILED;
    png_structp p=png_create_write_struct(PNG_LIBPNG_VER_STRING,NULL,png_error_quiet,png_warning_quiet);
    if(!p) {free(row);return FAILED;}
    png_infop info=png_create_info_struct(p);
    if(!info) {png_destroy_write_struct(&p,NULL);free(row);return FAILED;}
    if(setjmp(png_jmpbuf(p))) {png_destroy_write_struct(&p,&info);free(row);return FAILED;}
    png_init_io(p,stdout);png_set_compression_level(p,3);
    png_set_IHDR(p,info,f->width,f->height,8,PNG_COLOR_TYPE_RGB,PNG_INTERLACE_NONE,PNG_COMPRESSION_TYPE_BASE,PNG_FILTER_TYPE_BASE);
    png_write_info(p,info);
    for(uint32_t y=0;y<f->height;y++) {
        const unsigned char *src=data+f->offset+(size_t)y*f->pitch;
        for(uint32_t x=0;x<f->width;x++) {
            if(f->format==DRM_FORMAT_RGB565) {
                uint16_t v;memcpy(&v,src+2*x,2);
                row[3*x]=((v>>11)&31)*255/31;row[3*x+1]=((v>>5)&63)*255/63;row[3*x+2]=(v&31)*255/31;
            } else {
                if(f->format==DRM_FORMAT_ARGB8888 && src[4*x+3]!=255)png_error(p,"alpha");
                row[3*x]=src[4*x+2];row[3*x+1]=src[4*x+1];row[3*x+2]=src[4*x];
            }
        }
        png_write_row(p,row);
    }
    png_write_end(p,info);png_destroy_write_struct(&p,&info);free(row);
    return fflush(stdout)?FAILED:0;
}
int main(int argc,char **argv) {
    (void)argv;
    alarm(10);
    struct rlimit memory={256u*1024u*1024u,256u*1024u*1024u},cpu={8,8},core={0,0};
    if(argc!=1 || setrlimit(RLIMIT_AS,&memory)||setrlimit(RLIMIT_CPU,&cpu)||setrlimit(RLIMIT_CORE,&core)||!authorize())return DENIED;
    clearenv();umask(077);
    /* Do not consume stdin or retain inherited non-standard descriptors. */
    close(0);if(close_range(3,~0U,0))return FAILED;
    struct frame f;unsigned char *data=NULL;
    int rc=capture(&f,&data);
    if(!drop()) {free(data);return DENIED;}
    if(!rc && f.format==DRM_FORMAT_ARGB8888) {
        for(uint32_t y=0;y<f.height;y++) for(uint32_t x=0;x<f.width;x++)
            if(data[f.offset+(size_t)y*f.pitch+4*x+3]!=255)rc=UNSUPPORTED;
    }
    if(!rc)rc=encode(&f,data);
    free(data);return rc;
}
