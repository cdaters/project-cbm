/* GPL-2.0-only: test translation unit includes the GPL component.
 * No test hooks or environmental overrides enter the shipped executable. */
#define drmModeGetResources mock_resources
#define drmModeFreeResources mock_free_resources
#define drmModeGetConnectorCurrent mock_connector
#define drmModeFreeConnector mock_free_connector
#define drmModeGetEncoder mock_encoder
#define drmModeFreeEncoder mock_free_encoder
#define drmModeGetCrtc mock_crtc
#define drmModeFreeCrtc mock_free_crtc
#define drmModeObjectGetProperties mock_properties
#define drmModeFreeObjectProperties mock_free_properties
#define drmModeGetProperty mock_property
#define drmModeFreeProperty mock_free_property
#define drmModeGetPlaneResources mock_planes
#define drmModeFreePlaneResources mock_free_planes
#define drmModeGetPlane mock_plane
#define drmModeFreePlane mock_free_plane
#define drmModeGetFB2 mock_fb
#define drmModeFreeFB2 mock_free_fb
#define drmCloseBufferHandle mock_close_handle
#define drmPrimeHandleToFD mock_prime
#define ioctl mock_ioctl
#define main capture_main
#include "../../components/pcbm-kms-capture/capture.c"
#undef main
#include <assert.h>
#include <stdarg.h>
#include <sys/wait.h>
static int connectors=1,plane_count=1,flip=0,gets=0,mode_change=0,format_change=0,missing=0,permission=0,sync_failure=0,handles_closed=0;
static const char *property_names[]={"ACTIVE","CTM","GAMMA_LUT","DEGAMMA_LUT","CRTC_X","CRTC_Y","CRTC_W","CRTC_H","SRC_X","SRC_Y","SRC_W","SRC_H","rotation","alpha"};
static uint64_t property_values[]={1,0,0,0,0,0,2,1,0,0,2<<16,1<<16,1,65535};
drmModeRes *mock_resources(int fd) {
    (void)fd;drmModeRes *r=calloc(1,sizeof(*r));r->count_connectors=connectors;
    r->connectors=calloc(2,4);r->connectors[0]=1;r->connectors[1]=2;return r;
}
void mock_free_resources(drmModeRes *r) {free(r->connectors);free(r);}
drmModeConnector *mock_connector(int fd,uint32_t id) {
    (void)fd;drmModeConnector *c=calloc(1,sizeof(*c));c->connector_id=id;c->connection=DRM_MODE_CONNECTED;c->encoder_id=3;return c;
}
void mock_free_connector(drmModeConnector *p) {free(p);}
drmModeEncoder *mock_encoder(int fd,uint32_t id) {(void)fd;(void)id;drmModeEncoder *e=calloc(1,sizeof(*e));e->crtc_id=4;return e;}
void mock_free_encoder(drmModeEncoder *p) {free(p);}
drmModeCrtc *mock_crtc(int fd,uint32_t id) {(void)fd;(void)id;drmModeCrtc *p=calloc(1,sizeof(*p));p->mode_valid=1;p->mode.hdisplay=2;p->mode.vdisplay=1;p->mode.clock=(mode_change && gets%2)?2:1;return p;}
void mock_free_crtc(drmModeCrtc *p) {free(p);}
drmModeObjectProperties *mock_properties(int fd,uint32_t obj,uint32_t type) {
    (void)fd;(void)obj;(void)type;drmModeObjectProperties *p=calloc(1,sizeof(*p));p->count_props=14;
    p->props=calloc(14,4);p->prop_values=calloc(14,8);
    for(int i=0;i<14;i++){p->props[i]=i+1;p->prop_values[i]=property_values[i];}return p;
}
void mock_free_properties(drmModeObjectProperties *p) {free(p->props);free(p->prop_values);free(p);}
drmModePropertyRes *mock_property(int fd,uint32_t id) {(void)fd;drmModePropertyRes *p=calloc(1,sizeof(*p));strcpy(p->name,property_names[id-1]);return p;}
void mock_free_property(drmModePropertyRes *p) {free(p);}
drmModePlaneRes *mock_planes(int fd) {(void)fd;drmModePlaneRes *p=calloc(1,sizeof(*p));p->count_planes=plane_count;p->planes=calloc(2,4);p->planes[0]=5;p->planes[1]=6;return p;}
void mock_free_planes(drmModePlaneRes *p) {free(p->planes);free(p);}
drmModePlane *mock_plane(int fd,uint32_t id) {(void)fd;drmModePlane *p=calloc(1,sizeof(*p));p->plane_id=id;p->crtc_id=4;p->fb_id=7+(flip?gets++:0);return p;}
void mock_free_plane(drmModePlane *p) {free(p);}
drmModeFB2 *mock_fb(int fd,uint32_t id) {(void)fd;(void)id;if(missing)return NULL;drmModeFB2 *p=calloc(1,sizeof(*p));p->width=2;p->height=1;p->pixel_format=(format_change && id%2)?DRM_FORMAT_NV12:DRM_FORMAT_XRGB8888;p->handles[0]=permission?0:1;p->pitches[0]=12;p->offsets[0]=4;return p;}
void mock_free_fb(drmModeFB2 *p) {free(p);}
int mock_close_handle(int fd,uint32_t handle) {(void)fd;(void)handle;handles_closed++;return 0;}
int mock_prime(int fd,uint32_t handle,uint32_t flags,int *prime) {
    (void)fd;(void)handle;(void)flags;*prime=memfd_create("pixels",MFD_CLOEXEC);
    unsigned char data[16]={0,0,0,0,0,0,255,0,0,255,0,0,0,0,0,0};
    assert(write(*prime,data,16)==16);return 0;
}
int mock_ioctl(int fd,unsigned long req,...) {(void)fd;(void)req;return sync_failure?-1:0;}
static void check_drop(void) {
    pid_t p=fork();assert(p>=0);
    if(!p) {assert(drop());assert(prctl(PR_GET_NO_NEW_PRIVS,0,0,0,0)==1);_exit(0);}
    int status;assert(waitpid(p,&status,0)==p);assert(WIFEXITED(status)&&WEXITSTATUS(status)==0);
}
int main(void) {
    const char *good="{\"schema_version\":1,\"owner_user\":\"pcbm\",\"appliance_user\":\"pcbm\",\"system_ready\":true,\"network_ready\":false,\"ready_services\":[\"ssh\",\"modem\",\"sharing\",\"discovery\"]}";
    assert(ready_policy(good));assert(!ready_policy("{\"system_ready\":true}"));
    assert(!ready_policy("{\"schema_version\":1,\"schema_version\":1}"));
    char invalid[512];snprintf(invalid,sizeof(invalid),"%s garbage",good);assert(!ready_policy(invalid));
    strcpy(invalid,good);char *word=strstr(invalid,"true");memcpy(word,"null",4);assert(!ready_policy(invalid));
    struct frame f;assert(describe(0,&f)==0);
    connectors=0;assert(describe(0,&f)==UNAVAILABLE);
    connectors=2;assert(describe(0,&f)==UNSUPPORTED);connectors=1;
    plane_count=2;assert(describe(0,&f)==UNSUPPORTED);plane_count=1;
    for(unsigned i=1;i<14;i++) {
        uint64_t old=property_values[i];property_values[i]++;
        assert(describe(0,&f)==UNSUPPORTED);property_values[i]=old;
    }
    drmModeFB2 *b=mock_fb(0,0);assert(describe(0,&f)==0);assert(layout(b,&f)==0);assert(f.size==16&&f.offset==4&&f.pitch==12);
    b->flags=DRM_MODE_FB_INTERLACED;assert(layout(b,&f)==UNSUPPORTED);b->flags=0;
    b->modifier=1;assert(layout(b,&f)==UNSUPPORTED);b->modifier=0;
    b->pixel_format=DRM_FORMAT_NV12;assert(layout(b,&f)==UNSUPPORTED);b->pixel_format=DRM_FORMAT_XRGB8888;
    b->pitches[0]=4;assert(layout(b,&f)==UNSUPPORTED);b->pitches[0]=12;
    b->handles[1]=2;assert(layout(b,&f)==UNSUPPORTED);b->handles[1]=0;
    b->offsets[0]=LIMIT;assert(layout(b,&f)==UNSUPPORTED);mock_free_fb(b);
    unsigned char *data=NULL;assert(pixels(0,&f,&data)==0);assert(data[6]==255&&data[9]==255);free(data);
    missing=1;assert(pixels(0,&f,&data)==CHANGED);missing=0;
    flip=1;gets=0;assert(pixels(0,&f,&data)==0);free(data);assert(gets==2);
    mode_change=1;gets=0;assert(pixels(0,&f,&data)==CHANGED);assert(gets==6);mode_change=0;
    format_change=1;gets=1;assert(pixels(0,&f,&data)==UNSUPPORTED);format_change=0;flip=0;
    permission=1;assert(pixels(0,&f,&data)==DENIED);permission=0;
    sync_failure=1;assert(pixels(0,&f,&data)==FAILED);sync_failure=0;
    assert(handles_closed==13);
    if(geteuid()==0)check_drop();else {fputs("root privilege-drop test required\n",stderr);return 1;}
    puts("PASS policy, display discovery, ambiguity, composition, transforms, format/stride/offset/modifier, ordinary page flips, bounded mode/stale retries, permissions, sync failure, GEM closure, permanent privilege drop");return 0;
}
