# Certificates for swidGenerator Integration Tests #

The certificates here have been generated using strongSwan's
[pki utility](https://wiki.strongswan.org/projects/strongswan/wiki/IpsecPKI)
using the following script:

    LIFETIME=3653
    export PASSWORD=...

    DN="C=CH, O=strongSwan, CN=swidGenerator Test CA"
    pki --gen --size 4096 --outform pem > swidgen-ca.key
    pki --self --ca --in swidgen-ca.key --type priv --dn "$DN" --lifetime $LIFETIME --outform pem > swidgen-ca.pem

    SAN="swidgen@strongswan.org"
    DN="C=CH, O=strongSwan, CN=$SAN"
    pki --gen --size 3072 --outform pem > swidgen.key
    pki --issue --in swidgen.key --type priv --cakey swidgen-ca.key --cacert swidgen-ca.pem --dn "$DN" --san "$SAN" --lifetime $LIFETIME --flag clientAuth --outform pem > swidgen.pem

    openssl pkcs12 -inkey swidgen.key -in swidgen.pem -out swidgen.pfx -export -aes128 -password env:PASSWORD
