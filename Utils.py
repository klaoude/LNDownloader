# -*- coding: utf-8 -*-

import re
import os
import json
from unidecode import unidecode

html_translation = [
    ("&quot;", u"\""), ("&laquo;", u"«"), ("&raquo;", u"»"), ("&lsaquo;", u"‹"), ("&rsaquo;", u"›"), 
    ("&ldquo;", u"“"), ("&rdquo;", u"”"), ("&bdquo;", u"„"), ("&apos;", u"'"), ("&lsquo;", u"‘"), 
    ("&rsquo;", u"’"), ("&sbquo;", u"‚"), ("&hellip;", u"…"), ("!", u"!"), ("&iexcl;", u"¡"), ("?", u"?"), 
    ("&iquest;", u"¿"), ("(", u"("), (")", u")"), ("[", u"["), ("]", u"]"), ("{", u"{"), ("}", u"}"), ("&uml;", u"¨"), 
    ("&acute;", u"´"), ("`", u"`"), ("^", u"^"), ("&circ;", u"ˆ"), ("~", u"~"), ("&tilde;", u"˜"), ("&cedil;", u"¸"), ("#", u"#"), 
    ("*", u"*"), (",", u","), (".", u"."), (":", u":"), (";", u";"), ("&middot;", u"·"), ("&bull;", u"•"), ("&macr;", u"¯"), ("&oline;", u"‾"), 
    ("-", u"-"), ("&ndash;", u"–"), ("&mdash;", u"—"), ("_", u"_"), ("|", u"|"), ("&brvbar;", u"¦"), ("&zwnj;", u"‌"), ("&zwj;", u"‍"), ("&dagger;", u"†"), 
    ("&Dagger;", u"‡"), ("&sect;", u"§"), ("&para;", u"¶"), ("&copy;", u"©"), ("&reg;", u"®"), ("&trade;", u"™"), ("&amp;", u"&"), ("@", u"@"), ("/", u"/"), 
    ("&loz;", u"◊"), ("&spades;", u"♠"), ("&clubs;", u"♣"), ("&hearts;", u"♥"), ("&diams;", u"♦"), ("&larr;", u"←"), ("&uarr;", u"↑"), ("&rarr;", u"→"), 
    ("&darr;", u"↓"), ("&harr;", u"↔"), ("&curren;", u"¤"), ("&euro;", u"€"), ("$", u"$"), ("&cent;", u"¢"), ("&pound;", u"£"), ("&yen;", u"¥"), ("&fnof;", u"ƒ"), 
    ("&aacute;", u"á"), ("&Aacute;", u"Á"), ("&acirc;", u"â"), ("&Acirc;", u"Â"), ("&agrave;", u"à"), ("&Agrave;", u"À"), ("&aring;", u"å"), ("&Aring;", u"Å"), 
    ("&atilde;", u"ã"), ("&Atilde;", u"Ã"), ("&auml;", u"ä"), ("&Auml;", u"Ä"), ("&aelig;", u"æ"), ("&AElig;", u"Æ"), ("&ccedil;", u"ç"), ("&Ccedil;", u"Ç"), 
    ("&eacute;", u"é"), ("&Eacute;", u"É"), ("&ecirc;", u"ê"), ("&Ecirc;", u"Ê"), ("&egrave;", u"è"), ("&Egrave;", u"È"), ("&euml;", u"ë"), ("&Euml;", u"Ë"), 
    ("&iacute;", u"í"), ("&Iacute;", u"Í"), ("&icirc;", u"î"), ("&Icirc;", u"Î"), ("&igrave;", u"ì"), ("&Igrave;", u"Ì"), ("&iuml;", u"ï"), ("&Iuml;", u"Ï"), 
    ("&ntilde;", u"ñ"), ("&Ntilde;", u"Ñ"), ("&oacute;", u"ó"), ("&Oacute;", u"Ó"), ("&ocirc;", u"ô"), ("&Ocirc;", u"Ô"), ("&ograve;", u"ò"), ("&Ograve;", u"Ò"), 
    ("&oslash;", u"ø"), ("&Oslash;", u"Ø"), ("&otilde;", u"õ"), ("&Otilde;", u"Õ"), ("&ouml;", u"ö"), ("&Ouml;", u"Ö"), ("&oelig;", u"œ"), ("&OElig;", u"Œ"), 
    ("&scaron;", u"š"), ("&Scaron;", u"Š"), ("&szlig;", u"ß"), ("&eth;", u"ð"), ("&ETH;", u"Ð"), ("&thorn;", u"þ"), ("&THORN;", u"Þ"), ("&uacute;", u"ú"), 
    ("&Uacute;", u"Ú"), ("&ucirc;", u"û"), ("&Ucirc;", u"Û"), ("&ugrave;", u"ù"), ("&Ugrave;", u"Ù"), ("&uuml;", u"ü"), ("&Uuml;", u"Ü"), ("&yacute;", u"ý"), 
    ("&Yacute;", u"Ý"), ("&yuml;", u"ÿ"), ("&Yuml;", u"Ÿ"), ("&alpha;", u"α"), ("&Alpha;", u"Α"), ("&beta;", u"β"), ("&Beta;", u"Β"), ("&gamma;", u"γ"), 
    ("&Gamma;", u"Γ"), ("&delta;", u"δ"), ("&Delta;", u"Δ"), ("&epsilon;", u"ε"), ("&Epsilon;", u"Ε"), ("&zeta;", u"ζ"), ("&Zeta;", u"Ζ"), ("&eta;", u"η"), 
    ("&Eta;", u"Η"), ("&theta;", u"θ"), ("&Theta;", u"Θ"), ("&iota;", u"ι"), ("&Iota;", u"Ι"), ("&kappa;", u"κ"), ("&Kappa;", u"Κ"), ("&lambda;", u"λ"), 
    ("&Lambda;", u"Λ"), ("&mu;", u"μ"), ("&Mu;", u"Μ"), ("&nu;", u"ν"), ("&Nu;", u"Ν"), ("&xi;", u"ξ"), ("&Xi;", u"Ξ"), ("&omicron;", u"ο"), ("&Omicron;", u"Ο"), 
    ("&pi;", u"π"), ("&Pi;", u"Π"), ("&rho;", u"ρ"), ("&Rho;", u"Ρ"), ("&sigma;", u"σ"), ("&sigmaf;", u"ς"), ("&Sigma;", u"Σ"), ("&tau;", u"τ"), ("&Tau;", u"Τ"), 
    ("&upsilon;", u"υ"), ("&Upsilon;", u"Υ"), ("&phi;", u"φ"), ("&Phi;", u"Φ"), ("&chi;", u"χ"), ("&Chi;", u"Χ"), ("&psi;", u"ψ"), ("&Psi;", u"Ψ"), ("&omega;", u"ω"),
     ("&Omega;", u"Ω"), ("&deg;", u"°"), ("&micro;", u"µ"), ("&lt;", u"<"), ("&gt;", u">"), ("&le;", u"≤"), ("&ge;", u"≥"), ("=", u"="), ("&asymp;", u"≈"), 
     ("&ne;", u"≠"), ("&equiv;", u"≡"), ("&plusmn;", u"±"), ("&minus;", u"−"), ("+", u"+"), ("&times;", u"×"), ("&divide;", u"÷"), ("&frasl;", u"⁄"), ("%", u"%"), 
     ("&permil;", u"‰"), ("&frac14;", u"¼"), ("&frac12;", u"½"), ("&frac34;", u"¾"), ("&sup1;", u"¹"), ("&sup2;", u"²"), ("&sup3;", u"³"), ("&ordm;", u"º"), 
     ("&ordf;", u"ª"), ("&fnof;", u"ƒ"), ("&prime;", u"′"), ("&Prime;", u"″"), ("&part;", u"∂"), ("&prod;", u"∏"), ("&sum;", u"∑"), ("&radic;", u"√"), 
     ("&infin;", u"∞"), ("&not;", u"¬"), ("&cap;", u"∩"), ("&int;", u"∫"), ("&rArr;", u"⇒"), ("&hArr;", u"⇔"), ("&forall;", u"∀"), ("&exist;", u"∃"), 
     ("&nabla;", u"∇"), ("&isin;", u"∈"), ("&ni;", u"∋"), ("&prop;", u"∝"), ("&ang;", u"∠"), ("&and;", u"∧"), ("&or;", u"∨"), ("&cup;", u"∪"), ("&there4;", u"∴"), 
     ("&sim;", u"∼"), ("&sub;", u"⊂"), ("&sup;", u"⊃"), ("&sube;", u"⊆"), ("&supe;", u"⊇"), ("&perp;", u"⊥"), ("&oplus;", u"⊕"), ("&thinsp;", u" "), 
     ("&ensp;", u" "), ("&emsp;", u" "), ("&weierp;", u"℘"), ("&image;", u"ℑ"), ("&real;", u"ℜ"), ("&crarr;", u"↵"), ("&lArr;", u"⇐"), ("&uArr;", u"⇑"), 
     ("&dArr;", u"⇓"), ("&empty;", u"∅"), ("&notin;", u"∉"), ("&lowast;", u"∗"), ("&cong;", u"≅"), ("&nsub;", u"⊄"), ("&otimes;", u"⊗"), ("&sdot;", u"⋅"), 
     ("&lceil;", u"⌈"), ("&rceil;", u"⌉"), ("&lfloor;", u"⌊"), ("&rfloor;", u"⌋"), ("&lang;", u"⟨"), ("&rang;", u"⟩"), ("&alefsym;", u"ℵ"), ("&thetasym;", u"ϑ"), 
     ("&piv;", u"ϖ"), ("&upsih;", u"ϒ"), ("&nbsp;", u""), ("&shy;", u""), ("&lrm;", u""), ("&rlm;", u"")
]

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """
  
  #  Populate the dictionary with object meta data 
  obj_dict = {
    "__class__": obj.__class__.__name__,
    "__module__": obj.__module__
  }

  #obj_dict = {}
  
  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)
  
  return obj_dict

def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")
        
        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")
        
        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)
        
        # Get the class from the module
        class_ = getattr(module,class_name)
        
        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj

def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def removeHttp(text):
    text = text.replace("</p>", "\n").replace("<br>", "\n").replace("<\\br>", "\n")
    text = re.sub(r"<(.*?)>", "", text)
    text = re.sub(r"&#[0-9]+", "", text)
    text = text.replace("[email;protected]", u"")
    for repl in html_translation:
        text = text.replace(repl[0], repl[1])
    return text

def Debug(text):
    print "\x1b[0;33;40m[DEBUG]{}\x1b[0m".format(text)

def CreateJSON(file):
    og_fr = Novel("Overgeared (FR)", "https://xiaowaz.fr/series-en-cours/overgeared/")

    op = Operation("refindall")
    op.re = r"href=\"([^ ]*?)\" title=\"(.*?)\""
    og_fr.AddFindChapters(op)

    op = Operation("resplit")
    op.re = r"<p(.*?)><strong>"
    op.maxsplit = 1
    op.keep = 2
    og_fr.AddRegex(op)

    op = Operation("split")
    op.string = "<div class=\"abh_box abh_box_down abh_box_business\">"
    op.keep = 0
    og_fr.AddRegex(op)

    xiao = NovelSite("xiaowaz.fr", "https://xiaowaz.fr/", [og_fr])


    og_en = Novel("Overgeared (EN)", "https://www.novelcool.com/novel/Overgeared.html", [], [], True)
    wuxiaworld = NovelSite("novelcool.com", "https://www.novelcool.com/", [og_en])

    with open(file, "w") as f:
        f.write(json.dumps([xiao, wuxiaworld], default=convert_to_dict, indent=4, sort_keys=True))

def LoadJSON(file):
    with open(file, "r") as f:
        json_content = f.read()
    return json.loads(json_content, object_hook=dict_to_obj)