/* Reference-only SDL observer. Never installed in the appliance. */
#define _GNU_SOURCE
#include <SDL.h>
#include <dlfcn.h>
#include <stdio.h>
void SDL_RenderPresent(SDL_Renderer *renderer)
{
    static unsigned frames;
    static void (*present)(SDL_Renderer *);
    if (!present) present = dlsym(RTLD_NEXT, "SDL_RenderPresent");
    if (++frames == 60) {
        SDL_Window *window = SDL_RenderGetWindow(renderer);
        SDL_RendererInfo info = {0}; SDL_Rect viewport = {0};
        SDL_DisplayMode mode = {0};
        int w=0,h=0,ow=0,oh=0,lw=0,lh=0;
        SDL_GetWindowSize(window,&w,&h);
        SDL_GetRendererOutputSize(renderer,&ow,&oh);
        SDL_RenderGetLogicalSize(renderer,&lw,&lh);
        SDL_RenderGetViewport(renderer,&viewport);
        SDL_GetRendererInfo(renderer,&info);
        SDL_GetCurrentDisplayMode(SDL_GetWindowDisplayIndex(window),&mode);
        fprintf(stderr,"CBM_REFERENCE driver=%s renderer=%s window=%dx%d output=%dx%d logical=%dx%d viewport=%d,%d,%d,%d flags=%u display=%dx%d@%d\n",
            SDL_GetCurrentVideoDriver(),info.name,w,h,ow,oh,lw,lh,
            viewport.x,viewport.y,viewport.w,viewport.h,SDL_GetWindowFlags(window),mode.w,mode.h,mode.refresh_rate);
    }
    present(renderer);
}
