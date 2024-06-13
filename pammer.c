// save this as pam_python.c
#include <security/pam_appl.h>
#include <security/pam_modules.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PYTHON_SCRIPT "~/facerec/facerec.py"

PAM_EXTERN int pam_sm_authenticate(pam_handle_t *pamh, int flags, int argc, const char **argv)
{
    int retval = PAM_AUTH_ERR;
    FILE *fp = popen("python3 " PYTHON_SCRIPT, "r");
    if (fp == NULL)
    {
        return retval;
    }

    char result[128];
    while (fgets(result, sizeof(result), fp) != NULL)
    {
        if (strstr(result, "SUCCESS") != NULL)
        {
            retval = PAM_SUCCESS;
            break;
        }
    }

    pclose(fp);
    return retval;
}

PAM_EXTERN int pam_sm_setcred(pam_handle_t *pamh, int flags, int argc, const char **argv)
{
    return PAM_SUCCESS;
}
