gcc -fPIC -shared -o pam_facerec.so pammer.c -lpam

sudo mv pam_facerec.so /lib/x86_64-linux-gnu/security/

auth       required   pam_facerec.so

