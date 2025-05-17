try:
    import os
    import re
    import requests
    from PIL import Image as ubah
    from bs4 import BeautifulSoup
    import img2pdf
    from concurrent.futures import as_completed
    from requests_futures.sessions import FuturesSession
    import dns.resolver
except:
    print('downloading package')
    import subprocess, sys

    folders = ''
    for i in __file__.split("/")[0:len(__file__.split("/"))-1]:
        folders = folders+i+'/'



    if folders == '':
        for i in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
            folders = folders+i+'\\'
    # print(folders)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r',f'{folders}requirements.txt'])
    print('downloaded package, run again')
    exit()



def change_dns_requests(dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]
    dns.resolver.override_system_resolver(resolver)

def restore_dns_requests():
    dns.resolver.restore_system_resolver()

change_dns_requests("8.8.8.8")

def hapusError(s):

    t = ""
    for i in s:
         
        
        if (i >= 'A' and i <= 'Z') or (i >= 'a' and i <= 'z') or (i ==' ') or (i >= '0' and i <= '9'):
            t += i
    return t

def cookies(kode):
    try:
        
        
        fps = requests.get(f"https://nhentai.net/g/{kode}/")
                        
        html = fps.text

        soup = BeautifulSoup(html, 'html.parser')
        oks = str(soup.find(itemprop="image"))
        oks = oks.split("/")
        server = (oks[2][1])

        obes = str(soup.get_text())
        obes = obes.split('»')
        nama = obes[0]

        path = (oks[4])

        soup = BeautifulSoup(html, 'html.parser')
        obes = str(soup.get_text())
        obes = obes.split(':')
        
        isi = 0
        for i in range(len(obes)):
            if obes[i].__contains__('Pages'):
                isi = (obes[i+1].replace('\t', '')).split('\n')[1]
        

        return [nama, server, path, isi]
    except Exception as e:
        print('error')
        print(e)
        
    


def download_image(nama_folder, url, file_name, ok_html):

    try:
        
        response = ok_html.get(url)
        
        

        
        if response.status_code == 200:
            with open(nama_folder+file_name, "wb") as f:
                f.write(response.content)
            return 1
        else:
            url = url[0:len(url)-3] + "jpg"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                with open(nama_folder+file_name, "wb") as f:
                    f.write(response.content)
                
                img = ubah.open(nama_folder+file_name)
                img.save(nama_folder+file_name)
                return 2
            else:
                print("request code error "+response.status_code)
                return 0
    except:
        print("something wrong")
        return 0

def jadi_gambar(tempat, berapa):
    gambars =[]
    for i in range(berapa):
        img = ubah.open(f"{tempat}{i+2}.png")
        gambars.append(img.convert("RGB"))
    return gambars

def mulai(nama_gambar, folders, url_database, berapa, nama_manga, async_working):
    

    if folders != "" :
        
        nama_folder = folders+"/"+nama_gambar+"/"
        try:
            os.mkdir(nama_folder)
        except:
            print('folder with that name already exist, overriding the folder')
            
    else : 
        
        nama_folder = ""
    try:
        print(f"you will download {berapa} page")
        i=0
        
        sessionx = FuturesSession(max_workers=async_working)

        futures=[]
        
        for ix in range(berapa):
            
            url = f"{url_database}{ix+1}.png"
            
            future = sessionx.get(url)
            future.i = ix+1
            futures.append(future)
        
        jpgsku=[]
        for future in as_completed(futures):
            resp = future.result()
            
            if resp.status_code != 200:
                url = f"{url_database}{future.i}.jpg"
                futurec = sessionx.get(url)
                futurec.i = future.i
                
                jpgsku.append(futurec)
            else:
                i+=1
                with open(nama_folder+f"{nama_gambar}{future.i}.png", "wb") as f:
                    f.write(resp.content)


        webpku=[]
        for future in as_completed(jpgsku):
            resp = future.result()
            
            # urlx = f"{url_database}{future.i}.jpg"
            
            
            if resp.status_code != 200:
                url = f"{url_database}{future.i}.webp"
                futurec = sessionx.get(url)
                futurec.i = future.i
                
                webpku.append(futurec)
                    
            else:
                with open(nama_folder+f"{nama_gambar}{future.i}.png", "wb") as f:
                    
                    f.write(resp.content)
                    

                    try:
                        img = ubah.open(nama_folder+f"{nama_gambar}{future.i}.png")
                        img.save(nama_folder+f"{nama_gambar}{future.i}.png")
                    except:
                        print('error converting image (it will continue)')
                    i+=1

        for future in as_completed(webpku):
            resp = future.result()

            if resp.status_code != 200:
                urlx = f"{url_database}{future.i}.webp"
                print(f"error while downloade image number {urlx}")

            else:
                with open(nama_folder+f"{nama_gambar}{future.i}.png", "wb") as f:
                    
                    f.write(resp.content)
                    

                    try:
                        img = ubah.open(nama_folder+f"{nama_gambar}{future.i}.png")
                        img.save(nama_folder+f"{nama_gambar}{future.i}.png")
                    except:
                        print('error converting image (it will continue)')
                    i+=1
        
        if i == berapa:       
            
            imgs = []
            for ixc in range(berapa):
                imgs.append(f"{nama_folder}{nama_gambar}{ixc+1}.png")
            
            if re.search('[a-zA-Z]', nama_gambar):
                nama_manga = nama_gambar
            with open(f"{nama_folder+hapusError(nama_manga)}.pdf","wb") as f:
                f.write(img2pdf.convert(imgs))
            print('completed converting img to pdf')
            
            for jalan in range(i):
                os.remove(f"{nama_folder}{nama_gambar}{jalan+1}.png")
            print("img deleted")
        
        else:
            print("something wrong while downloading")
    except Exception as e:
        print("fatal error")
        print(e)
        
    

def jalankan(kode_nuklirs):
    
    kode_nuklir = kode_nuklirs
    # print(kode_nuklirs)
    # try:
    folders=''
    


    for i in __file__.split("/")[0:len(__file__.split("/"))-1]:
        folders = folders+i+'/'



    if folders == '':
        for i in __file__.split("\\")[0:len(__file__.split("\\"))-1]:
            folders = folders+i+'\\'


    
    try:
        nama_manga, servers, paths, semua  = cookies(kode_nuklir)
    except:
        print('error while trying connect to database')
        exit()
    
    
    path =f"/galleries/{paths}/"
    url_database = f"https://i{servers}.nhentai.net"+path
    
    nama_manga = nama_manga.replace('\n', '')
    nama_manga = nama_manga[0:len(nama_manga)-1]
    print(f'Doujin Name \n"{nama_manga}"\n')
    
    mulai(kode_nuklir, folders, url_database, int(semua), nama_manga, int(6))


        
keco = input("give me code : ")

try:
    int(keco)
except:
    print('not a number')



change_dns_requests("8.8.8.8")
jalankan(keco)
