#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip3 install scapy')


# In[5]:


from scapy.all import *


# In[118]:


pcaps = rdpcap("imap_stream_0.pcap")


# In[308]:


# pcaps = rdpcap("imapPgpSignedSinglePayload_seq.pcap")


# ### Tabular view of the packet for analyzing relationship of all the fields with consecutive packets. 

# In[21]:


get_ipython().system('pip3 install scapy2dict')
get_ipython().system('pip3 install flatten_dict')
get_ipython().system('pip3 install openpyxl')


# In[37]:


import openpyxl
import pandas as pd
import numpy as np
from scapy2dict import to_dict
from flatten_dict import flatten


# In[29]:


dict(to_dict(pcaps[19]))


# In[30]:


flatten(dict(to_dict(pcaps[19])), reducer=lambda k1, k2: k2 if k1 is None else k1 + '.' + k2)


# In[119]:


df = pd.DataFrame([flatten(dict(to_dict(i)), reducer=lambda k1, k2: k2 if k1 is None else k1 + '.' + k2) for i in pcaps])
df.head(10)


# In[120]:


df.to_excel("imap_stream_0.xlsx", index=False)


# In[39]:


df.drop(df.index[df['Ethernet.dst'] == "4c:17:eb:64:16:49"], inplace=True)
df.to_excel("imap_only_data.xlsx", index = False)


# In[40]:


df.drop(df.index[df['Ethernet.src'] == "4c:17:eb:64:16:49"], inplace=True)
df.to_excel("imap_data_only.xlsx", index = False)


# In[262]:


df


# In[266]:


pcaps[19]


# #### PGP_signed email

# In[4]:



mailpayload = '''MIME-Version: 1.0
                Content-Type: multipart/signed; boundary="1790868a14";
                 protocol="application/pgp-signature"; micalg="pgp-sha512"
                From: Alice Lovelace <alice@openpgp.example>
                To: Bob Babbage <bob@openpgp.example>
                Date: Sun, 20 Oct 2019 09:18:11 -0400
                Subject: The FooCorp contract
                Message-ID: <signed@protected-headers.example>

                --1790868a14
                Content-Type: text/plain; charset="us-ascii"
                From: Alice Lovelace <alice@openpgp.example>
                To: Bob Babbage <bob@openpgp.example>
                Date: Sun, 20 Oct 2019 09:18:11 -0400
                Subject: The FooCorp contract
                Message-ID: <signed@protected-headers.example>

                Bob, we need to cancel this contract.

                Please start the necessary processes to make that happen today.

                Thanks, Alice
                -- 
                Alice Lovelace
                President
                OpenPGP Example Corp

                --1790868a14
                content-type: application/pgp-signature

                -----BEGIN PGP SIGNATURE-----

                wnUEARYKAB0FAl2sXpMWIQTrhbtfozp14V6UTmPyMVUMT0fjjgAKCRDyMVUMT0fj
                jq3uAP4/K66bZXT4jFsmKLztz2Ihxjftgf3TaeD2uL05yWdJAQEAjRdWIh35C6MP
                utqkLnFeLpkTwrMnncdF/G+so/yXvQA=
                =UMd4
                -----END PGP SIGNATURE-----

                --1790868a14-- 
                '''


# #### PGP_Encrypted email 

# In[222]:


mailpayload = '''MIME-Version: 1.0
Content-Type: multipart/encrypted; boundary="bcde3ce988";
 protocol="application/pgp-encrypted"
From: Alice Lovelace <alice@openpgp.example>
To: Bob Babbage <bob@openpgp.example>
Date: Mon, 21 Oct 2019 07:18:11 -0700
Message-ID: <signed+encrypted@protected-headers.example>
Subject: ...

--bcde3ce988
content-type: application/pgp-encrypted

Version: 1

--bcde3ce988
content-type: application/octet-stream

-----BEGIN PGP MESSAGE-----

wV4DR2b2udXyHrYSAQdAifmSGlN6dUG8WjtsDsVf3RoFUu69cEhUQyVMaUBEaSAw
EAtGxmoM2YY6y/87UXI2USJMj9PiFn7RuV0pAFVT6NwMAY1JgLX5qoSdKXuLZ9CA
wcDMA3wvqk35PDeyAQv9HNVhvGMSyCXZjsu5LlLGPF/6XHnk3PtunCo8GpUd7Mg9
zVDS0zK+dtePYHNgKZ47KLDBgu6XInVBWeeSkImaWjFirTmqp/GP20urKQ/phSkC
vI88cEH+fCqeFxDcL5tb0RLm3/iv707CHvoOM2qCbV8WDSSvNY2FGlJZqqGO3mkE
VhZFytVop12c/L5+PltIS0/P25KMoSuIIb9xenAncyLZ1a2M/NsgZjBqWeXFfQnZ
ssMK1xOvNIYNxUzEws+U6un74OE5sBZeZCvM/nIf50iXvEQMxoc/MX2XFUA9Scid
+bmy9nZCit0KQNk4ikrshgtxmG6xJfMv1IpnscQwMy9KfOAhnrVWFVHpzr+K7mXb
yHHF4Ov1Cl2FvwHU6DujaoApkn/xg5BjbRZxfRfVF7LvZ3UJJ/v1XzGLv5LTL8Fr
1S+Ql69M8yvftMiZ799dNgOT7jc4CY5yN7P2YQn5Z3Nm/gUWcGwuqwQecw0hs/87
yCQzkDHAC62LL6+zHqc20sHbAeuQHcGttI9Vu8rEO+5OeDr3WjTB/UXvLKr/G9ty
LUpaYYwFtNgMaRAg0niMV9xfwTFjLBmNkq/8N0mAOsZSO9lMZyUIfBiFbw5yWNzx
TuKxZymZ3ts6ywvKOgzLNgF+AdtTQk5nkNIsh7Fd02RSl9heF3t47FXVSvBSo5KI
FXuznjzK7VNl8fTp9MpBwp00Dai3jtKGQ3/XGiD4l/wa/QxfffojPAZ9UZpgA2Xx
Uw3W4+zCNZNJ35QME6I2ysKwbgAQGFeKM57lLXrmIJWU7KEIDnc1MCBwsSt50yB8
kIdSPXxK/Jon2wbATUN8Uuo3oLA2dpH8XncjrkqTooNjkK3uPrGNphDBVSMA5W5Z
deHc9NmzETXLBPysc0LHWMUO8g4YnWB4sLq9ZBxTYYX9CYRJvdB8EZN4Dq+IUDVK
W7Hu8oFkPRqU7oVa+utiZq5YvTXbIMJBWdUa8r8zlwz0jVsUJGBIPDWhs8Yse2JX
54dNJRAy2X5M3KM1S2Aat1gHl35cft5pLYLp5/gs7GYgybhYfgXbcbBHE6/XTAtg
L7ZbzN+AEDu24uPQaTN5jUA8MfQIkksRgIhZN3N8NBVltv4t+tbtIiaLLaQ/7Wdd
X0BINwZxhBZHEtjljqf4VE4RlWpMriW+ezcrPU3zEcM62knjeCLCh9iseAuz1J1o
R1o4DKwlVY9dJZigguO9kzz+K9n1/mpn8orV9kn5FyH9vs9ZF+RQiSHgpoZ3TKER
iy4T7WPV1WzyPSTmlKktOGjgJ5nszKw8YarMjtXYiPNOShBWuBTxBeSyjCLhZ85m
YAhS1znrJ9CzX3jjaZTHTd/5gYN7wVByUlw9OkyN2QQRFl6fg1xN6Tb79oGxDqh/
BHb6PBgDtwnGmHdDmw==
=rTjd
-----END PGP MESSAGE-----

--bcde3ce988--'''


# #### PGP_Signed_html

# In[215]:


mailpayload = '''Content-Type: multipart/signed; boundary="c72d4fa142";
 protocol="application/pgp-signature"; micalg="pgp-sha512"

--c72d4fa142
Content-Type: multipart/mixed; boundary="6ae0cc9247"
From: Alice Lovelace <alice@openpgp.example>
To: Bob Babbage <bob@openpgp.example>
Date: Mon, 21 Oct 2019 07:18:11 -0700
Subject: BarCorp contract signed, let's go!
Message-ID: <unfortunately-complex@protected-headers.example>

--6ae0cc9247
content-type: text/rfc822-headers; protected-headers="v1"
Content-Disposition: inline

Subject: BarCorp contract signed, let's go!

--6ae0cc9247
Content-Type: multipart/mixed; boundary="8dfc0e9ecf"

--8dfc0e9ecf
Content-Type: multipart/alternative; boundary="32c4d5a901"

--32c4d5a901
Content-Type: text/plain; charset="us-ascii"

Hi Bob!

I just signed the contract with BarCorp and they've set us up with
an account on their system for testing.

The account information is:

        Site: https://barcorp.example/
    Username: examplecorptest
    Password: correct-horse-battery-staple

Please get the account set up and apply the test harness.

Let me know when you've got some results.

Thanks, Alice
-- 
Alice Lovelace
President
OpenPGP Example Corp

--32c4d5a901
Content-Type: text/html; charset="us-ascii"

<html><head></head><body><p>Hi Bob!
</p><p>
I just signed the contract with BarCorp and they've set us up with
 an account on their system for testing.
</p><p>
The account information is:
</p><dl>
<dt>Site</dt><dd>
<a href="https://barcorp.example/">https://barcorp.example/</a>
</dd>
<dt>Username</dt><dd><tt>examplecorptest</tt></dd>
<dt>Password</dt><dd>correct-horse-battery-staple</dd>
</dl><p>
Please get the account set up and apply the test harness.
</p><p>
Let me know when you've got some results.
</p><p>
Thanks, Alice<br/>
-- <br/>
Alice Lovelace<br/>
President<br/>
OpenPGP Example Corp<br/>
</p></body></html>

--32c4d5a901--

--8dfc0e9ecf
Content-Type: text/x-diff; charset="us-ascii"
Content-Disposition: inline; filename="testharness-config.diff"

diff -ruN a/testharness.cfg b/testharness.cfg
--- a/testharness.cfg
+++ b/testharness.cfg
@@ -13,3 +13,8 @@
 endpoint = https://openpgp.example/test/
 username = testuser
 password = MJVMZlHR75mILg
+
+[barcorp]
+endpoint = https://barcorp.example/
+username = examplecorptest
+password = correct-horse-battery-staple

--8dfc0e9ecf--

--6ae0cc9247--

--c72d4fa142
content-type: application/pgp-signature

-----BEGIN PGP SIGNATURE-----

wnUEARYKAB0FAl2tviMWIQTrhbtfozp14V6UTmPyMVUMT0fjjgAKCRDyMVUMT0fj
jrR3AP9H2o1HBGLwkz5qzBgGmXsXLrc2xbluWtYmiDQcnq3e9QEA+DaBG1gEXasg
7OfAEqT4DrOivtNo18CxpIPrskgOXws=
=Ul2/
-----END PGP SIGNATURE-----

--c72d4fa142--
'''


# ### S/MIME signed and encrypted SMTP Email 

# In[10]:


mailpayload='''MIME-Version: 1.0
Content-Transfer-Encoding: base64
Content-Type: application/pkcs7-mime; name="smime.p7m";
 smime-type="enveloped-data"
From: Alice Lovelace <alice@smime.example>
To: Bob Babbage <bob@smime.example>
Date: Wed, 27 Nov 2019 01:24:00 -0700
Message-ID: <smime-sign+enc+legacy-disp@protected-headers.example>
Subject: ...

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
mi1JBjXLAT3pEJDh8b3Lpgw=
'''


# In[6]:


def changePayload(pcaps, pktNo, newPayload,append=False):
    oldSize = len(pcaps[pktNo]["Raw"].load)
    print (pktNo,"--------")
    # change payload and insert byte
    if (type(newPayload)==str):
        newPayload = "\r\n".join([ i.strip() for i in newPayload.split("\n")])
    elif (type(newPayload)==bytes):
        print ("payload in byte.... Processing ..... ")
    else:
        print ("The new payload should be string or byte format. You inserted "+ type(newPayload) + " .")
        return pcaps
#     print(newPayload)
    pcaps[pktNo]["Raw"].load = newPayload
#     print ("payload length : ",len(pcaps[pktNo]["Raw"].load))
    #change IP len value
    pcaps[pktNo]["IP"].len = len(pcaps[pktNo]["IP"])
    
    #change seq and ack values of the next packets
    pktSynSrt = str(pcaps[pktNo]["TCP"].seq)[:3]
    if (append==False):
        diffLen = len(pcaps[pktNo]["Raw"].load) - oldSize
    elif (append==True):
        diffLen = len(pcaps[pktNo]["Raw"].load)
        
        
    print ("payload length difference : ",diffLen)
    for pcap in pcaps[pktNo+1:]:
        if (str(pcap["TCP"].seq)[:3]==pktSynSrt):
            pcap["TCP"].seq += diffLen
        elif (str(pcap["TCP"].ack)[:3]==pktSynSrt):
            pcap["TCP"].ack += diffLen
            
    # for packet append id of IP also should be incremented
    if (append==True):
        ipIdSrt = str(pcaps[pktNo]["IP"].id)[:2]
        if (pktNo==19):    #---------------------------------->>>> this is hardcoded--->changes needed
            return pcaps
            print ("-----------first fragmented pkt------------")
        for pcap in pcaps[pktNo:]:
            if (str(pcap["IP"].id)[:2]==ipIdSrt):
                pcap["IP"].id = pcap["IP"].id+1
            
    return pcaps


# In[ ]:


fileIn = "imap_stream_0.pcap"
fileOut = "smtp_smime_signed_encrypted.pcap"


# In[228]:


pcaps = rdpcap(fileIn)
pcaps[19].show()


# ### This is for non-fragmented payload

# In[36]:


pcaps = changePayload(pcaps, 19, mailpayload, False)
pcaps = changePayload(pcaps, 11, "MAIL FROM:<alice@smime.example> SIZE="+str(len(bytes(mailpayload, "utf-8")))+"\r\n",False)
pcaps = changePayload(pcaps, 13, b'RCPT TO:<bob@smime.example>\r\n',False)

# by deleting checksum field scapy will recalculate checksums
for i in range(len(pcaps)):
    del pcaps[i]["IP"].chksum
    del pcaps[i]["TCP"].chksum
#     pcaps[i].show2()
wrpcap(fileOut, pcaps)


# ### This part is for fragmented payload

# In[229]:


import copy
pcaps = list(pcaps)
maxLoadLen = 1000
for i in range(int(len(mailpayload)/maxLoadLen)+1):
#     print(i)
#     print(mailpayload[i*maxLoadLen:(i+1)*maxLoadLen])
    if (i == int(len(mailpayload)/maxLoadLen)):
        break
    tmpPcap = copy.copy(pcaps[19])
    tmpPcap["TCP"].flags = "A"
    pcaps.insert(19, tmpPcap)
    
pktNo = 19
for i in range(int(len(mailpayload)/maxLoadLen)+1):
    newPayload = mailpayload[i*maxLoadLen:(i+1)*maxLoadLen]
    if (i==int(len(mailpayload)/maxLoadLen)):
        pcaps = changePayload(pcaps, pktNo+i, newPayload,False)
        print("last fragment no: "+str(i))
    else:
        pcaps = changePayload(pcaps, pktNo+i, newPayload,True)
        print("fragment no: "+str(i))
        
        


# In[230]:


pktNo=21
ipIdSrt = str(pcaps[pktNo]["IP"].id)[:2]
for pcap in pcaps[pktNo:]:
    if (str(pcap["IP"].id)[:2]==ipIdSrt):
        pcap["IP"].id = pcap["IP"].id+1


# Rectify from and to email address in different packet.

# In[ ]:


pcaps = changePayload(pcaps, 11, "MAIL FROM:<alice@smime.example> SIZE="+str(len(bytes(mailpayload, "utf-8")))+"\r\n",False)
pcaps = changePayload(pcaps, 13, b'RCPT TO:<bob@smime.example>\r\n',False)


# This part is to recalculate TCP and IP checksums. And save the final packet.

# In[232]:


for i in range(len(pcaps)):
    del pcaps[i]["IP"].chksum
    del pcaps[i]["TCP"].chksum
wrpcap("smtp_pgp_encrypted_frag.pcap",pcaps)


# In[12]:


pcaps[20].show()


# In[231]:


def printraw(pcaps):
    maxlen = 0
    line=0
    for packet in pcaps:
        line+=1
        try:
            print (packet["Raw"].load)
            maxlen = max(len(packet["Raw"].load), maxlen)
            print(line, len(packet["Raw"].load))
        except:
            continue
printraw(pcaps)


# ## After changing  "Frame Length" of "Data Link Layer" of the packets (where payload has been changed) using Terminal tool ghex. Now, correct email to and from in other payloads

# In[ ]:





# In[ ]:





# In[ ]:




