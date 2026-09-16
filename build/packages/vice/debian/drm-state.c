/* SPDX-License-Identifier: GPL-2.0-or-later
 * Copyright 2026 Project CBM contributors. Private engineering read-only DRM diagnostics.
 * No modesetting, authentication/master acquisition, EDID, serials or root.
 */
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <xf86drmMode.h>
int main(int argc, char **argv)
{
    (void)argv;
    if (argc != 1 || geteuid() == 0 || access("/etc/pcbm/engineering-poc", F_OK)) return 1;
    int first=1;
    puts("{\"connectors\":[");
    for (int card=0; card<16; ++card) {
        char path[32]; snprintf(path,sizeof path,"/dev/dri/card%d",card);
        int fd=open(path,O_RDONLY|O_CLOEXEC);
        if (fd<0) continue;
        drmModeRes *resources=drmModeGetResources(fd);
        if (!resources) { close(fd); continue; }
        for (int i=0;i<resources->count_connectors && i<16;++i) {
            drmModeConnector *c=drmModeGetConnectorCurrent(fd,resources->connectors[i]);
            if (!c) continue;
            printf("%s{\"card\":%d,\"connector_id\":%u,\"type\":%u,\"type_id\":%u,\"connected\":%s",
                first?"":",",card,c->connector_id,c->connector_type,c->connector_type_id,
                c->connection==DRM_MODE_CONNECTED?"true":"false");
            first=0;
            drmModeEncoder *e=c->encoder_id?drmModeGetEncoder(fd,c->encoder_id):NULL;
            drmModeCrtc *crtc=e && e->crtc_id?drmModeGetCrtc(fd,e->crtc_id):NULL;
            if (crtc && crtc->mode_valid) {
                printf(",\"active\":{\"width\":%u,\"height\":%u,\"refresh_hz\":%u,\"clock_khz\":%u,\"htotal\":%u,\"vtotal\":%u,\"flags\":%u,\"crtc_width\":%u,\"crtc_height\":%u,\"x\":%u,\"y\":%u}",
                    crtc->mode.hdisplay,crtc->mode.vdisplay,crtc->mode.vrefresh,
                    crtc->mode.clock,crtc->mode.htotal,crtc->mode.vtotal,crtc->mode.flags,
                    crtc->width,crtc->height,crtc->x,crtc->y);
            } else printf(",\"active\":null");
            puts("}");
            if (crtc) drmModeFreeCrtc(crtc);
            if (e) drmModeFreeEncoder(e);
            drmModeFreeConnector(c);
        }
        drmModeFreeResources(resources); close(fd);
    }
    puts("]}");
    return 0;
}
