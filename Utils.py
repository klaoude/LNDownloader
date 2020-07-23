import re
import os

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
    text = text.replace("&nbsp;", " ").replace("&amp;", "&")
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