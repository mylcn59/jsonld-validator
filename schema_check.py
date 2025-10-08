import requests, json, sys, os, time
from extruct import extract
from w3lib.html import get_base_url

TIMEOUT = int(os.getenv("SCHEMA_TIMEOUT", "20"))
RETRY   = int(os.getenv("SCHEMA_RETRY", "2"))
ORG_ID  = os.getenv("ORG_ID", "https://www.icgiyimozel.com/#organization")
ALLOW_NO_PRODUCT_ON_LIST = True  # Kategori sayfasında Product zorunlu değil; ItemList yeter

def must(cond, msg):
    if not cond:
        print("❌", msg); sys.exit(1)

def warn(cond, msg):
    if not cond:
        print("⚠️", msg)

def fetch(url):
    for attempt in range(RETRY+1):
        try:
            r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent":"SchemaBot/1.0"})
            if r.status_code == 200:
                return r.text
            else:
                print(f"Attempt {attempt+1}: HTTP {r.status_code} for {url}")
        except Exception as e:
            print(f"Attempt {attempt+1}: error {e}")
        time.sleep(1.0)
    must(False, f"URL alınamadı: {url}")

def is_numberlike(x):
    try:
        float(str(x).replace(",", "."))
        return True
    except:
        return False

def check_offer_node(node):
    must(node.get("priceCurrency"), "Offer.priceCurrency yok")
    must(node.get("availability"), "Offer.availability yok")
    must(node.get("price") is not None, "Offer.price yok")
    must(is_numberlike(node.get("price")), "Offer.price sayı değil")
    seller = node.get("seller", {})
    must(isinstance(seller, dict) and seller.get("@id")==ORG_ID, f"Offer.seller.@id beklenen değil ({seller})")

def check_product(p):
    must(p.get("@type")=="Product", "Product @type yok/yanlış")
    must(p.get("name"), "Product.name yok")
    brand = p.get("brand", {})
    must(isinstance(brand, dict) and brand.get("name"), "Brand.name yok")
    offers = p.get("offers", {})
    must(offers, "Product.offers yok")
    if offers.get("@type") == "AggregateOffer":
        sub = offers.get("offers", [])
        must(isinstance(sub, list) and len(sub)>0, "AggregateOffer.offers boş")
        check_offer_node(sub[0])
    else:
        check_offer_node(offers)

def check_itemlist(il):
    must(il.get("@type")=="ItemList", "ItemList @type yok/yanlış")
    items = il.get("itemListElement", [])
    must(isinstance(items, list) and len(items)>0, "ItemList boş")
    for idx, li in enumerate(items, 1):
        it = li.get("item", {})
        must(it.get("@type")=="Product", f"ItemListElement[{idx}].item Product değil")
        # Liste sayfasında Product’ı hafif kontrol edelim:
        check_product(it)

def inspect(url):
    html = fetch(url)
    data = extract(html, base_url=get_base_url(html, url), syntaxes=['json-ld'])["json-ld"]
    must(len(data)>0, "Sayfada JSON-LD bulunamadı")

    found_product=False
    found_itemlist=False

    for node in data:
        ntype = node.get("@type")
        if ntype == "Product":
            found_product = True
            check_product(node)
        elif ntype == "ItemList":
            found_itemlist = True
            check_itemlist(node)
        # Organization/WebSite @id yoksa uyarı niteliğinde
        if ntype == "Organization":
            oid = node.get("@id")
            warn(oid == ORG_ID, f"Organization @id beklenen değil: {oid}")

    # Sayfa tipine göre minimum beklenti:
    # - Ürün sayfası: Product şart
    # - Kategori sayfası: ItemList şart
    if "/urunleri" in url or "/modelleri" in url:
        must(found_itemlist, "Kategori sayfasında ItemList bulunamadı")
    else:
        must(found_product, "Ürün sayfasında Product bulunamadı")

    print(f"✅ OK: {url} (Product:{found_product}, ItemList:{found_itemlist})")

def main():
    path = os.getenv("URLS_FILE", "tests/urls.txt")
    with open(path, "r", encoding="utf-8") as f:
        urls = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    must(len(urls)>0, "urls.txt boş")
    for u in urls:
        inspect(u)

if __name__ == "__main__":
    main()
