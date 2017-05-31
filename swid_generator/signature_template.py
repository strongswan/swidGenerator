SIGNATURE = '<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">' \
            '<SignedInfo>' \
            '<CanonicalizationMethod Algorithm="http://www.w3.org/2006/12/xml-c14n11"/>' \
            '<SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>' \
            '<Reference>' \
            '<Transforms>' \
            '<Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>' \
            '<Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>' \
            '</Transforms>' \
            '<DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>' \
            '<DigestValue />' \
            '</Reference>' \
            '</SignedInfo>' \
            '<SignatureValue />' \
            '<KeyInfo><X509Data />' \
            '</KeyInfo>' \
            '</Signature>'
