import hashlib
import random 
from math import pow
class dilKontrol:
    def init(self,metin):
        self.metin=metin
    def cumlelereBol(self,metin):
        metin=metin.replace("!",".")
        metin=metin.replace("?",".")
        parcalananMetin=metin.split(".")
        cumlesayi=len(parcalananMetin)
        if cumlesayi>1:
            cumlesayi=cumlesayi-1
        return parcalananMetin,cumlesayi
    def kelimelereBol(self,metin):
        parcalananCumle=metin.split()
        return parcalananCumle,len(parcalananCumle)
    def sesliHarfBul(self,metin):
        sesli_harf = 'AEIİOÖUÜaeıioöuü'
        sayac=0
        for i in metin:
            if i in sesli_harf:
                sayac +=1
        return sayac
    def buyukunluUyumu(self,metin):
        sesliharfler='AEIİOÖUÜaeıioöuü'
        kalinunluler='AIOUaıou'
        inceunluler='EİÜÖeiüö'
        kelimeler=metin.split()
        uyanlar=[]
        uymayanlar=[]
        tekhece=[]
        for i in range(len(kelimeler)):
            icindekisesli=[]
            for j in range(len(kelimeler[i])):
                if kelimeler[i][j] in sesliharfler:
                    icindekisesli.append(kelimeler[i][j])
            if len(icindekisesli)==1:
                print("-> {} gibi tek heceli kelimelerde büyük ünlü uyumu aranmaz".format(kelimeler[i]))
                tekhece.append(kelimeler[i])
            else:
                if list(icindekisesli)[0] in kalinunluler:
                    if set(icindekisesli).issubset(set(kalinunluler)):
                        uyanlar.append(kelimeler[i])
                    else:
                        uymayanlar.append(kelimeler[i])
                else:
                    if set(icindekisesli).issubset(set(inceunluler)):
                        uyanlar.append(kelimeler[i])
                    else:
                        uymayanlar.append(kelimeler[i])                                    
        return len(uyanlar),uyanlar,len(uymayanlar),uymayanlar
class sifrelemeYontemleri:
    def init(self, metin):
        self.metin=metin
    def ElGamal(self,metin):
        def gcd(a,b):
            if a<b:
                return gcd(b,a)
            elif a%b ==0:
                return b
            else:
                return gcd(b,a%b)
        def gen_key(q):
            key=random.randint(pow(10,20),q)
            while gcd(q,key)!=1:
                key=random.randint(pow(10,20),q)
            return key
        def power(a,b,c):
            x=1
            y=a
            while b>0:
                if b%2==0:
                    x=(x*y)%c
                y=(y*y)%c
                b=int(b/2)
            return x%c
        def encrypt(msg,q,h,g):
            en_msg=[]
            #gizli anahtar
            k=gen_key(q)
            s=power(h,k,q)
            p=power(g,k,q)
            for i in range(0,len(msg)):
                en_msg.append(msg[i])
            print("g^k used : ", p)
            print("g^ak used : ", s)
            for i in range(0, len(en_msg)):
                en_msg[i] = s * ord(en_msg[i])
            return en_msg,p
        def decrypt(en_msg,p,key,q):
            dr_msg=[]
            h=power(p, key, q)
            for i in range(0, len(en_msg)):
                dr_msg.append(chr(int(en_msg[i]/h)))
            return dr_msg
        q=random.randint(pow(10, 20), pow(10, 50))
        g=random.randint(2, q)  
        key=gen_key(q)
        h=power(g, key, q)
        print("g used : ", g)
        print("g^a used : ", h)
        en_msg, p = encrypt(metin, q, h, g)
        dr_msg = decrypt(en_msg, p, key, q)
        dmsg = ''.join(dr_msg)
        return dmsg
    def RC4(self,metin):
        anahtar = input("[*] Anahtarı giriniz:")
        InitialStateVector = [] #S[i]
        TemporaryVector = [] #K[i]
        for i in range(256):
            InitialStateVector.append(i)
            TemporaryVector.append(anahtar[i % len(anahtar)])
        soru = input("Initial State Vector değeri gösterilsin mi?(e/h)\r\n")
        if(soru == "e"):
            print("Initial State Vector:")
            for i in range(256):
                print(InitialStateVector[i], end=" ")
        soru = input("\r\nTemporary Vector değeri gösterilsin mi?(e/h)\r\n")
        if(soru == "e"):
            print("Temporary Vector:")
            for i in range(256):
                print(TemporaryVector[i], end=" ")
        #Adım:2
        j = 0
        for i in range(256):
            j = (j + InitialStateVector[i] + ord(TemporaryVector[i])) % 256
            deger1 = InitialStateVector[j]
            deger2 =  InitialStateVector[i]
            InitialStateVector[j] = deger2
            InitialStateVector[i] = deger1
        print()
        soru = input("Permuted State Vector değeri gösterilsin mi?(e/h)\r\n")
        if(soru == "e"):
            print("Permuted State Vector:")
            for i in range(256):
                print(InitialStateVector[i], end=" ")
        #Adım:3
        i = 0
        j = 0
        k=[]
        C = []
        for l in range(len(metin)):
            i = (i + 1) % 256
            j = (j + InitialStateVector[i])  % 256
            deger1 = InitialStateVector[i]
            deger2 = InitialStateVector[j]
            k.append( InitialStateVector[((InitialStateVector[i] + InitialStateVector[j]) % 256)])
            p = ord(metin[l])
            c = bin(p ^ k[l])
            C.append(int(c,2))
        return C
    def md5(self,metin):
        hash_object = hashlib.md5(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    def SHA1(self,metin):
        hash_object = hashlib.sha1(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    def SHA224(self,metin):
        hash_object = hashlib.sha224(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    def SHA256(self,metin):
        hash_object = hashlib.sha256(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    def SHA384(self,metin):
        hash_object = hashlib.sha384(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    def SHA512(self,metin):
        hash_object = hashlib.sha512(metin.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
class help:
    Uyari1="-> Dil kontrol sinifi her hangi bir metni cümlelere ve kelimelere bölebilir.\n-> Metin içerisinde kac adet cümle, kelime, unlu harf oldugunu denetler.\n-> Buyuk unlu uyumu kontrolu yapar.\n\n-> Sifreleme sinifi ise metni hash, simetrik ve asimetrik sifreleme yöntemleri ile sifrelemektedir."
    Uyari2="-> El Gamal Asimetrik - RC4 Simetrik - Diger islemler hash sifrelemedir.\n-> Baslangicde girilen metni sifreleyebilirsiniz."
def main():
    metin=input('Metni Giriniz: ')
    try:
        islem=int(input('1- Dil Kontrol\n2- Sifreleme\n3- Help\nYapilacak islemi seciniz:'))
        if islem == 1:
            nesne=dilKontrol()
            cumleArray,cumleSayisi=nesne.cumlelereBol(metin)
            print(cumleArray,"Cümle sayisi =",cumleSayisi)
            kelimeArray,kelimeSayisi=nesne.kelimelereBol(metin)
            print(kelimeArray,"Kelime sayisi =",kelimeSayisi)
            sesliHarfSayisi=nesne.sesliHarfBul(metin)
            print("Sesli harf adedi =",sesliHarfSayisi)
            uyanSayisi,uyanlar,uymayanSayisi,uymayanlar=nesne.buyukunluUyumu(metin)
            print("\n**Büyük ünlü uyumuna uyan kelime sayisi: ",uyanSayisi)
            print("-> Uyanlar:",uyanlar)
            print("**Büyük ünlü uyumuna uymayan kelime sayisi: ",uymayanSayisi)
            print("-> Uymayanlar:",uymayanlar)
            main()
        elif islem == 2:
            sifrelemeNesnesi=sifrelemeYontemleri()
            islem1=input('Yontem Sec\n1- El Gamal\n2- RC4\n3- MD5\n4- SHA1\n5- SHA224\n6- SHA256\n7- SHA384\n8- SHA512\n9- Yardim\nSecim:')
            print("\nMetin-> ",metin)
            if islem1=="1":  
                sifrelenenString=sifrelemeNesnesi.ElGamal(metin)
                print("Cozulen Metin-> ",sifrelenenString)
            elif islem1=="2":
                sifrelenenString=sifrelemeNesnesi.RC4(metin)
                print("RC4-> ",sifrelenenString)
            elif islem1=="3":
                sifrelenenString=sifrelemeNesnesi.md5(metin)
                print("MD5 Encryption-> ",sifrelenenString)
            elif islem1=="4":
                sifrelenenString=sifrelemeNesnesi.SHA1(metin)
                print("SHA1 Encryption-> ",sifrelenenString)
            elif islem1=="5":
                sifrelenenString=sifrelemeNesnesi.SHA224(metin)
                print("SHA224 Encryption-> ",sifrelenenString)
            elif islem1=="6":
                sifrelenenString=sifrelemeNesnesi.SHA256(metin)
                print("SHA256 Encryption-> ",sifrelenenString)
            elif islem1=="7":
                sifrelenenString=sifrelemeNesnesi.SHA384(metin)
                print("SHA384 Encryption-> ",sifrelenenString)
            elif islem1=="8":
                sifrelenenString=sifrelemeNesnesi.SHA512(metin)
                print("SHA512 Encryption-> ",sifrelenenString)
            elif islem1=="9":
                print(help.Uyari2)
                main()
            else:
                print("Hatali giris yapildi...")
                main()
            main()
        else:
            print(help.Uyari1)
            main()
    except ValueError:
        print("\nSayi girmelisin. Lutfen adimlari izle.")
        main()
try:
  print("***Hazirlayanlar***\n1 - Yunus Emre Demirel - 182805015\n2 - Alpay Duymaz - 182805002\n3 - Aydin Can - 182805005\n")
except:
  print("Program Calismadi. Kutuphaneler yuklenmemis olabilir.")
finally:
  if __name__ == "__main__":main()