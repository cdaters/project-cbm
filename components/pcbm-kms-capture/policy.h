/* SPDX-License-Identifier: GPL-2.0-only
 * Project CBM contributors, 2026. Fixed activation-policy grammar. */
#include <ctype.h>
static void space(const char **p) { while (isspace((unsigned char)**p)) ++*p; }
static int token(const char **p, const char *s) {
    space(p); size_t n=strlen(s);
    if (strncmp(*p,s,n)) return 0;
    *p+=n; return 1;
}
/* No escapes, duplicates, unknown keys, or permissive substring matching.
 * This is deliberately only the existing six-key activation policy, not JSON
 * supplied by the caller. A future policy change must update this gate. */
static int ready_policy(const char *p) {
    unsigned seen=0;
    const char *keys[]={"\"schema_version\"","\"owner_user\"","\"appliance_user\"",
        "\"system_ready\"","\"network_ready\"","\"ready_services\""};
    if (!token(&p,"{")) return 0;
    for (;;) {
        unsigned k;
        for(k=0;k<6;k++) if(token(&p,keys[k])) break;
        if(k==6 || (seen&(1u<<k)) || !token(&p,":")) return 0;
        seen|=1u<<k;
        if(k==0) { if(!token(&p,"1")) return 0; }
        else if(k==1 || k==2) { if(!token(&p,"\"pcbm\"")) return 0; }
        else if(k==3) { if(!token(&p,"true")) return 0; }
        else if(k==4) { if(!token(&p,"true") && !token(&p,"false")) return 0; }
        else {
            if(!token(&p,"[")) return 0;
            if(!token(&p,"]")) for(;;) {
                if(!token(&p,"\"ssh\"") && !token(&p,"\"sharing\"") &&
                   !token(&p,"\"discovery\"") && !token(&p,"\"modem\"")) return 0;
                if(token(&p,"]")) break;
                if(!token(&p,",")) return 0;
            }
        }
        if(token(&p,"}")) break;
        if(!token(&p,",")) return 0;
    }
    space(&p); return seen==63 && *p==0;
}
