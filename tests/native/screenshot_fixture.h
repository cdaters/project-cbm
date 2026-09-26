/* GPL-2.0-only. Build-time test boundary, never included in a shipped package.
 * Included immediately before production main; replace only pixel acquisition. */
static int fixture_capture(struct frame *f,unsigned char **out) {
    *f=(struct frame){.width=2,.height=1,.format=DRM_FORMAT_XRGB8888,.pitch=12,.offset=4,.size=16};
    *out=calloc(1,16);if(!*out)return FAILED;
    (*out)[6]=255;(*out)[9]=255;return 0;
}
#define capture fixture_capture
