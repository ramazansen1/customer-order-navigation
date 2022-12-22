# 1 → Kütüphaneleri import edelim
import requests, urllib.parse, time, json
from datetime import datetime

# 2 → Customers API için gerekli URL girelim
urlCustomers = "https://northwind.netcore.io/customers.json"

# 3 → Customers API için GET request
rCustomers = requests.get(urlCustomers)

# 4 → if  case, bu kısımda her hangi bir kod değişikliği yapmayın lütfen
if not rCustomers.status_code == 200:
    raise Exception("API Bağlantı Sorunu. Status code: {}. Text: {}".format(
        rCustomers.status_code, rCustomers.text))

# 5 → Response içeriği print et referans amaçlı
# print(rCustomers.text)

# 6 → Response icerigi json data formatına encode et
jsonCustomers = rCustomers.json()

# 7 → Orders API için gerekli URL'leri girelim
urlOrders = "https://northwind.netcore.io/query/orders.json"

# 8 → Orders API için GET request
rOrders = requests.get(urlOrders)

# 9 → if  case, bu kısımda her hangi bir kod değişikliği yapmayın lütfen
if not rOrders.status_code == 200:
    raise Exception("API Bağlantı Sorunu. Status code: {}. Text: {}".format(
        rOrders.status_code, rOrders.text))

# 10 → Response içeriği print et referans amaçlı
#print(rOrders.text)

# 11 → response icerigi json data formatına encode et
jsonOrders = rOrders.json()

# 12 → Mapquest API için gerekli URL'leri girelim
mainMapApiUrl="https://www.mapquestapi.com/directions/v2/route?"

# 13 → Mapquest Credential için; token, key... hazırlıkları yapalım
mapApiKey="kacYZJzzAbzZmlwmbGMAjgM4Po2KzJmd"


# 14 → UI manipulasyonu. Output anında 15 karakterden uzun metinler için manipulasyon yapalım
def metinKontrol(metin):
    if len(str(metin))>16:
        charControl = str(metin).replace(metin[15:],"...")
        return charControl
    else:
        return metin

# 15 → Müşterileri listeleyelim
def musteriListele():
    dataKeys = ["id", "companyName", "contactName", "address", "country", "city"]
    print("Müşteri Listesi")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")
    print("|ID      |CompanyName            |ContactName            |Address                |Country                |City                   |")
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")

    for i in jsonCustomers["results"]:
        customerDatas = [metinKontrol(i[key]) for key in dataKeys]
        print("|{0:<8}|{1:<23}|{2:<23}|{3:<23}|{4:<23}|{5:<23}|".format(*customerDatas))
 
    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")

# 16 → Müşterileri Id'ye göre arama yapalım
def musteriAra(musteriId):
    keys = [
            "id", "companyName", "contactName", "contactTitle",
            "address", "city", "postalCode", "country", "phone", "fax"  
            ]
    values = [
            "Id", "Firma Adı", "Müşteri Adı", "İş Disiplini",
            "Adres", "Şehir", "Posta Kodu", "Ülke", "Telefon", "Fax"
            ]
    
    for customer in jsonCustomers["results"]:
        if customer['id']==musteriId:
            print(f"{musteriId} ID'li müşteri bulundu. Detay Listesi")
            print("==========================")
            for key, value in zip(keys, values):
                try:
                    print(f"{value : <20}: {customer[key]}")
                except:
                    print(f"{value : <20}: ...")


                # print(f'{key}\t: {value}')
            # print(f'ID\t\t: {i["id"]}\nFirma Adı\t: {i["companyName"]}\nMüşteri Adı\t: {i["contactName"]}\nİş Disiplini\t: {i["contactTitle"]}\nAdres\t\t: {i["address"]}\n'
            #       f'Şehir\t\t: {i["city"]}\nPosta Kodu\t: {i["postalCode"]}\nÜlke\t\t: {i["country"]}\nTelefon\t\t: {i["phone"]}\nFax\t\t: {i["fax"]}')          
            break
    else:
        print(f"{musteriId} ID'li müşteri bulunamadı")

# 17 → Siparişleri listeleyelim
def siparisListele():  
    dataKeys = ["id", "customerId", "shipAddress", "shipCity", "shipCountry"]
    print("Sipariş Listesi")
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+-----------------------+")
    print("|ID      |CustomerId     |OrderDate                      |ShipAddress            |ShipCity               |ShipCountry            |")
    print("+--------+---------------+-------------------------------+-----------------------+-----------------------+-----------------------+")
    for order in jsonOrders["results"]:
        epochSaniye = int(order['orderDate'][6:15])
        gunumuzZamani = time.strftime("%a %b %d %H:%M:%S %Y", time.gmtime(epochSaniye))
        orderDatas = [metinKontrol(order[key]) for key in dataKeys]
        orderDatas.append(gunumuzZamani)
        print("|{0:<8}|{1:<15}|{5:<31}|{2:<23}|{3:<23}|{4:<23}|".format(*orderDatas))

    print("+--------+-----------------------+-----------------------+-----------------------+-----------------------+-----------------------+")

# 18 → Sipariş Id'ye göre arama yapalım
def siparisAra(siparisId):
    keys = [
            "id", "customerId", "shipName", "contactName", "orderDate",
            "shipAddress", "shipCity", "shipCountry"  
            ]
    values = [
            "Sipariş Id", "Müşteri Id", "Firma Adı", "Müşteri Adı",
            "Sipariş Tarihi", "Adres", "Şehir", "Ülke"
            ]
    for order in jsonOrders["results"]:
        if order['id']==siparisId:

            print(f"{siparisId} ID'li sipariş bulundu. Detay Listesi")
            print("="*75)

            for key, value in zip(keys, values):
                if key == "contactName":
                    for customer in jsonCustomers["results"]:
                        if customer["id"] == order["customerId"]:
                            print(f"{value : <20}: {customer[key]}")

                elif key == "orderDate":
                    epochSaniye = int(order['orderDate'][6:15])
                    gunumuzZamani = time.strftime("%a %b %d %H:%M:%S %Y", time.gmtime(epochSaniye))
                    print(f"{value : <20}: {gunumuzZamani}")
                else:
                    print(f"{value : <20}: {order[key]}")
            print("="*75)
             
            nereye = order["shipCity"]         
            cevap = input(f"Kargo Rotasını {nereye.upper()} Şehri İçin Görmek İster misiniz? [e/E] :")
            if cevap.lower()=="e":
                while True:                    
                    print(f"Varış Noktası {nereye} için Rota Hesaplanacak")
                    nereden = input("Nereden Çıkacak: ")
                    mapapiUrl = mainMapApiUrl + urllib.parse.urlencode({"key" : mapApiKey, "from" : nereden, "to": nereye})
                    mapapiRoute = requests.get(mapapiUrl).json()
                    break
                print("="*75)
                print(f"Kargo Rotası {nereden} den/dan, {nereye} e/a/ye/ya")
                print(f"Toplam süre\t: {mapapiRoute['route']['formattedTime']}")
                print(f"Kilometre\t: {mapapiRoute['route']['distance']*1.61:.2f}")
                print("="*75)

                for navi in mapapiRoute["route"]["legs"][0]["maneuvers"]:
                    print(f"{navi['narrative']}, ({navi['distance']*1.61:.2f}) km.")
                
                print("="*75)

            break
            
    else:
        print(f"{siparisId} ID'li sipariş bulunamadı")


# 19 → menu
while True:
    for i in range(5):
        print()
    secim = int(input("""
    Seçiminiz:
    [1]     → MÜŞTERİ LİSTELE
    [2]     → MÜŞTERİ ARA <MÜŞTERİ ID'E GÖRE>
    [3]     → SİPARİŞ LİSTELE
    [4]     → SİPARİŞ ARA <SİPARİŞ ID'E GÖRE>
    [5]     → ÇIK
    """))
    if secim==1:
        musteriListele()
    elif secim==2:
        musteriId = input("Lütfen Müşteri Id Giriniz: ")
        musteriAra(musteriId)
    elif secim==3:
        siparisListele()
    elif secim==4:
        siparisId = int(input("Lütfen Sipariş Id Giriniz: "))
        siparisAra(siparisId)
    elif secim==5:
        break
    else:
        print("Hatalı seçim!")