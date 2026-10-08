"""Vocabulary for the synthetic search benchmark (Latin, Roman-Urdu and Urdu names).

Everything here is synthetic. Word pairs (Roman Urdu, Urdu script) let one name exist in both scripts so that a
cross-script variant row can be generated. Spelling of the Urdu side is good enough for trigram and token statistics;
it is NOT a reviewed lexicon (a native speaker must review before any of it is used as a synonym table).
"""

# (roman urdu, urdu script)
PAIRS = """noor نور|madina مدینہ|makkah مکہ|bismillah بسم اللہ|faisal فیصل|gulshan گلشن|bahar بہار|karim کریم|rehmat رحمت|rehman رحمان
mehran مہران|shalimar شالیمار|badshahi بادشاہی|lahori لاہوری|pakistan پاکستان|punjab پنجاب|sindh سندھ|hunza ہنزہ|swat سوات|ravi راوی
chenab چناب|zamzam زمزم|al ال|ghazi غازی|shaheen شاہین|sitara ستارہ|chand چاند|suraj سورج|taj تاج|mahal محل
darbar دربار|sultan سلطان|nawab نواب|malik ملک|raja راجہ|khan خان|butt بٹ|chaudhry چوہدری|sheikh شیخ|mian میاں
qureshi قریشی|siddiqui صدیقی|ansari انصاری|hashmi ہاشمی|usmani عثمانی|alvi علوی|awan اعوان|gondal گوندل|bhatti بھٹی|cheema چیمہ
virk ورک|dar ڈار|mughal مغل|pathan پٹھان|baloch بلوچ|saeed سعید|ahmed احمد|ali علی|hassan حسن|hussain حسین
usman عثمان|omar عمر|bilal بلال|zaid زید|fatima فاطمہ|ayesha عائشہ|zainab زینب|khadija خدیجہ|amina آمنہ|sana ثنا
iqra اقرا|iqbal اقبال|jinnah جناح|quaid قائد|azam اعظم|millat ملت|watan وطن|awami عوامی|qaumi قومی|markazi مرکزی
jadeed جدید|naya نیا|purana پرانا|asli اصلی|sasta سستا|behtareen بہترین|super سپر|star سٹار|royal رائل|golden گولڈن
silver سلور|diamond ڈائمنڈ|pearl پرل|green گرین|blue بلو|white وائٹ|city سٹی|central سینٹرل|new نیو|modern ماڈرن
grand گرینڈ|palace پیلس|plaza پلازہ|garden گارڈن|park پارک|view ویو|paradise پیراڈائز|continental کانٹینینٹل|sunrise سن رائز|crown کراؤن
sialkot سیالکوٹ|lahore لاہور|karachi کراچی|islamabad اسلام آباد|rawalpindi راولپنڈی|faisalabad فیصل آباد|multan ملتان|peshawar پشاور|quetta کوئٹہ|gujranwala گوجرانوالہ
hyderabad حیدرآباد|murree مری|bahawalpur بہاولپور|sargodha سرگودھا|gujrat گجرات|sukkur سکھر|larkana لاڑکانہ|mardan مردان|abbottabad ایبٹ آباد|jhelum جہلم
dil دل|jaan جان|zindagi زندگی|khushi خوشی|umeed امید|roshan روشن|sabz سبز|laal لال|neela نیلا|safaid سفید
bagh باغ|chaman چمن|phool پھول|gulab گلاب|mogra موگرا|chambeli چنبیلی|kamal کمال|jamal جمال|akram اکرم|asghar اصغر
shan شان|aan آن|izzat عزت|waqar وقار|himmat ہمت|taqat طاقت|ittefaq اتفاق|ekta یکتا|insaf انصاف|sadaqat صداقت""".replace("\n", "|").split("|")
PAIRS = [tuple(p.split(" ", 1)) for p in PAIRS if p.strip()]

# English brand words (Latin names)
EN_BRANDS = """royal pearl golden silver star crown grand city central new modern green blue white red sunrise sunset ocean river
mountain valley garden park view paradise continental imperial classic elite prime premier supreme global united national
metro urban capital heritage legacy pioneer summit horizon harbour bright smart quick fast easy best top first one alpha
beta delta omega nova apex zenith vertex orbit lotus jasmine rose lily orchid maple cedar pine oak willow falcon eagle
lion tiger panther swan dove phoenix crescent diamond emerald ruby sapphire topaz amber ivory pearl coral jade onyx
union alliance liberty freedom unity trust faith hope grace harmony serenity tranquil comfort cosy sunny breeze bay
lake hill ridge heights tower plaza court square avenue boulevard street road lane gate bridge crossing junction""".split()

# (english, roman urdu, urdu) type nouns for generic concepts
NOUNS = [
 ("traders","traders","ٹریڈرز"),("brothers","brothers","برادرز"),("sons","sons","سنز"),("enterprises","enterprises","انٹرپرائزز"),
 ("company","company","کمپنی"),("store","store","سٹور"),("mart","mart","مارٹ"),("center","markaz","مرکز"),("clinic","clinic","کلینک"),
 ("medical","medical","میڈیکل"),("pharmacy","pharmacy","فارمیسی"),("hospital","hospital","ہسپتال"),("workshop","workshop","ورکشاپ"),
 ("tailors","tailors","ٹیلرز"),("bakers","bakers","بیکرز"),("foods","foods","فوڈز"),("restaurant","restaurant","ریسٹورنٹ"),
 ("motors","motors","موٹرز"),("auto","auto","آٹو"),("parts","parts","پارٹس"),("electric","electric","الیکٹرک"),("electronics","electronics","الیکٹرانکس"),
 ("furniture","furniture","فرنیچر"),("garments","garments","گارمنٹس"),("textile","textile","ٹیکسٹائل"),("mills","mills","ملز"),
 ("builders","builders","بلڈرز"),("construction","construction","کنسٹرکشن"),("engineering","engineering","انجینئرنگ"),("associates","associates","ایسوسی ایٹس"),
 ("services","services","سروسز"),("solutions","solutions","سولوشنز"),("international","international","انٹرنیشنل"),("industries","industries","انڈسٹریز"),
 ("works","works","ورکس"),("shop","dukan","دکان"),("factory","karkhana","کارخانہ"),("dispensary","dawakhana","دوا خانہ"),("bazaar","bazaar","بازار"),
 ("house","ghar","گھر"),("cloth house","cloth house","کلاتھ ہاؤس"),("sweets","sweets","سویٹس"),("jewellers","jewellers","جیولرز"),("optical","optical","آپٹیکل"),
 ("dental","dental","ڈینٹل"),("lab","lab","لیب"),("diagnostics","diagnostics","ڈائگناسٹکس"),("tyres","tyres","ٹائرز"),("hardware","hardware","ہارڈ ویئر"),
 ("paints","paints","پینٹس"),("sanitary","sanitary","سینیٹری"),("tiles","tiles","ٹائلز"),("steel","steel","سٹیل"),("printers","printers","پرنٹرز"),
 ("laundry","laundry","لانڈری"),("salon","salon","سیلون"),("gym","gym","جم"),("travels","travels","ٹریولز"),("cargo","cargo","کارگو"),
 ("courier","courier","کوریئر"),("tuition","tuition","ٹیوشن"),("academy","academy","اکیڈمی"),("college","college","کالج"),("institute","institute","انسٹیٹیوٹ"),
 ("consultants","consultants","کنسلٹنٹس"),("law","law","لاء"),("chambers","chambers","چیمبرز"),("security","security","سیکیورٹی"),("agency","agency","ایجنسی"),
]

# pilot list types: (slug, english nouns, roman nouns, urdu nouns)
PILOT_NOUNS = {
 "hotels": ([ "hotel","guest house","inn","residency","lodge" ], ["hotel","hotal","guest house","musafir khana","residency"], ["ہوٹل","گیسٹ ہاؤس","مسافر خانہ","ریذیڈنسی"]),
 "schools": ([ "school","grammar school","public school","academy","montessori" ], ["school","grammar school","public school","academy","montessori"], ["سکول","گرامر سکول","پبلک سکول","اکیڈمی","مدرسہ"]),
 "plumbers": ([ "plumber","plumbing services","sanitary works","plumbers" ], ["plumber","plumbing services","sanitary works","nal saaz"], ["پلمبر","پلمبنگ سروسز","سینیٹری ورکس","نل ساز"]),
 "surgical": ([ "surgical instruments","surgical works","surgical industries","surgico","medical instruments" ], ["surgical instruments","surgical works","surgical industries","jarrahi auzar","surgico"], ["سرجیکل انسٹرومنٹس","سرجیکل ورکس","سرجیکل انڈسٹریز","جراحی اوزار"]),
}

# syllables for pseudo surnames and company names (roman, urdu)
SYLL = [("ma","ما"),("lik","لک"),("sha","شا"),("fiq","فق"),("ra","را"),("him","ہم"),("ka","کا"),("mal","مل"),("su","سو"),("dha","دھا"),
 ("na","نا"),("wa","وا"),("zi","زی"),("ba","با"),("rak","رک"),("tar","تر"),("ja","جا"),("han","ہن"),("gir","گیر"),("pa","پا"),
 ("ti","تی"),("la","لا"),("shi","شی"),("qa","قا"),("sim","سم"),("ha","ہا"),("ni","نی"),("ya","یا"),("da","دا"),("ri","ری"),
 ("fa","فا"),("saj","سج"),("jid","جد"),("nas","ناس"),("ur","ور"),("kha","کھا"),("lid","لد"),("mu","مو"),("rad","راد"),("bu","بو"),
 ("dil","دل"),("kar","کر"),("san","سن"),("mat","مت"),("gul","گل"),("bak","بک"),("yar","یار"),("zar","زر"),("pur","پور"),("ab","اب")]

# Places. Pakistan real provinces and cities with relative weight (share of Pakistan entries), others synthetic.
PK_CITIES = [  # (province, city, weight)
 ("sindh","karachi",14),("punjab","lahore",12),("islamabad","islamabad",5),("punjab","rawalpindi",5),("punjab","faisalabad",4),
 ("punjab","sialkot",3.5),("punjab","multan",3),("kpk","peshawar",3),("punjab","gujranwala",3),("balochistan","quetta",2),
 ("sindh","hyderabad",2),("punjab","bahawalpur",1.2),("punjab","sargodha",1.2),("punjab","gujrat",1.2),("sindh","sukkur",0.8),
 ("sindh","larkana",0.6),("kpk","mardan",1),("kpk","abbottabad",0.8),("punjab","jhelum",0.7),("punjab","murree",0.4),
]
