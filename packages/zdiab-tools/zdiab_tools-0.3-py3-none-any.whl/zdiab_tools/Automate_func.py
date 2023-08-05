from rasa.shared.nlu.training_data.formats.rasa_yaml import RasaYAMLReader, RasaYAMLWriter
import rasa
import pickle


# It creates a class called Automate.
class Automate():
    STR_Policy = """\npolicies:
# # No configuration for policies was provided. The following default policies were used to train your model.
# # If you'd like to customize them, uncomment and adjust the policies.
# # See https://rasa.com/docs/rasa/policies for more information.
    - name: MemoizationPolicy
    - name: RulePolicy
    - name: UnexpecTEDIntentPolicy
      max_history: 5
      epochs: 140
    """
    def __init__(self):
                
  
        return("Great !!!")

    #######################################
    ## Fonction pour ajouter avec rasa YAML 
    #######################################

    def add_rasa_file(yaml_string, path):
        """
        The function takes a string in YAML format and a path to a file and writes the YAML string to the
        file
        
        :param yaml_string: This is the string format YAML
        :param path: The path to the file you want to write to
        """

        f=RasaYAMLReader()
        training_data = f.reads(yaml_string)
        d=RasaYAMLWriter()
        print(d.dump(path,training_data))

    ## Domain
    #####################################################
    ## Fonction pour ajouter **Action, intent, enteties**
    #####################################################
    def add_intent(name, list_action):
        """
        :param name: The name of the intent
        :param list_action: a list of data
        :return: A string.
        """
  
        str = "\n"
        str += name +":\n"
        for n in list_action:
            str += "- " + n + "\n"
        return str

    ## Domain
    ##############################
    ## Fonction pour ajouter forms
    ##############################
    def add_forms(name, list_slots):
        """
        It takes a name and a list of slots and returns a string that can be used in the domain.yml file
        
        :param name: the name of the form (ex: "product_form")
        :param list_slots: a list of slots
        :return: A string that can be used in the domain.yml file
        """
        
        str = "\nforms:\n  "
        str += name +":\n    "
        str += "required_slots:\n    "
        for n in list_slots:
            str += "- " + n + "\n    "
        return str

    ## Domain
    ##############################
    ## Fonction pour ajouter slots
    ##############################
    def add_slot(name_form, list_slots):
        """
        It takes a list of slot names and returns a string that contains the YAML code for the slots
        
        :param name_form: the name of the form (ex: "product_form")
        :param list_slots: a list of slots
        :return: A string that contains the YAML code for the slots
        """
       
        str = "\nslots:\n"
        for n in list_slots:
            str += "  " + n +":\n"
            str += "    type: text\n"
            str += "    influence_conversation: true\n"
            str += "    mappings:\n"
            str += "      - type: from_text\n"
            str += "        conditions:\n"
            str += "         - active_loop: " + name_form + "\n"
            str += "           requested_slot: " + n + "\n"
        return str


    ## Domain
    ##################################################
    ## Fonction pour **responses** dans fichier domain
    ##################################################
    def add_responses(list_name, list_action):
        """
        It takes two lists of equal length, and returns a string that contains the first element of the
        first list, followed by the first element of the second list, followed by the second element of the
        first list, followed by the second element of the second list, and so on
        
        :param list_name: a list of utter_.. (e.g. "utter_greet")
        :param list_action: a list of text data (e.g. "Hello, how can I help you?")
        :return: A string that contains the first element of the first list, followed by the first element
        of the second list, followed by the second element of the first list, followed by the second
        element of the second list, and so on.
        """
        
        str = "\nresponses:\n  "
        if (len(list_action) == len(list_name)):
            for n in list_name:
                for m in list_action:
                    str += n + ":\n  "
                    str += "- text: " + m + "\n  "
        else:
            print("les deux lists sont de taille differents")
        return str

    ###########################################
    ## Fonction pour l'ecriture dans un fichier
    ###########################################

    def add_file(path, str):
        """
        This function takes a path and a string as arguments and appends the string to the file at the given
        path
        
        :param path: This is the location of the file ex: "C:/Users/user_name/Desktop/test/config.yml"
        :param str: the string to be added to the file
        """
       
        f = open(path, "a")
        f.write(str)
        f.close()
        print("fichier est modifier !!")


    #####################################################
    #####################################################
    #####################################################

    #####################
    ## Fonction ALTER !!!
    #####################

    ## Domain
    #####################################################
    ## Fonction pour ALTER **Action, intent, enteties**
    #####################################################
    def alter_intent(name, list_action):
        """
        It takes a list of strings and returns a list of strings.
        
        :param name: The name of the intent, action, or entity
        :param list_action: a list of data
        :return: A list of lists.
        """
 
        str = ""
        for n in list_action:
            str += "- " + n + "\n"
        l = [name, str]
        return l


    ## Domain
    ##################################
    ## Fonction pour ALTER **slots**
    ##################################
    def alter_slot(name_form, list_slots):
        """
        It takes a list of slot names and returns a list of two elements: the first element is the string
        "slots" and the second element is a string that contains the yaml code for the slots
        
        :param name_form: the name of the form (ex: "product_form")
        :param list_slots: a list of slots
        :return: A list of two elements. The first element is the string "slots" and the second element is
        a string that contains the slots.
        """
     
        str = ""
        for n in list_slots:
            str += "  " + n +":\n"
            str += "    type: text\n"
            str += "    influence_conversation: true\n"
            str += "    mappings:\n"
            str += "      - type: from_text\n"
            str += "        conditions:\n"
            str += "         - active_loop: " + name_form + "\n"
            str += "           requested_slot: " + n + "\n"
        name = "slots"
        l = [name, str]
        return l


    ## Domain
    ##################################
    ## Fonction pour ALTER **forms**
    ##################################
    def alter_forms(name, list_slots):
        """
        :param name: the name of the form (e.g. "product_form")
        :param list_slots: a list of slots
        :return: A list of two elements. The first element is the name of the form, and the second element
        is a string.
        """
   
        str = ""
        for n in list_slots:
            str += "    - " + n + "\n"
        l = [name, str]
        return l


    ## Domain
    ##########################################################
    ## Fonction pour ALTER **responses** dans fichier domain
    ##########################################################
    def alter_responses(list_name, list_action):
        """
        It takes two lists as input, and returns a list of two elements. The first element is the string
        "responses", and the second element is a string that contains the contents of the two lists
        
        :param list_name: a list of utter_.. (e.g. "utter_greet")
        :param list_action: a list of examples (e.g:  "Bonjour comment je peux vous aider?")
        :return: A list of two strings.
        """

        str = ""
        if (len(list_action) == len(list_name)):
            for i in range(len(list_name )):
                str += "  " + list_name[i] + ":\n"
                str += "  - text: " + list_action[i] + "\n"
        else:
            print("les deux lists sont de taille differents")
        name = "responses"
        l = [name, str]
        return l


    ## Domain
    ##### Alter FILE
    ###############################################################################
    ## Fonction pour MODIFIER Intent, Action, Entities et Responses dans un fichier
    ###############################################################################


    def alter_file(path, li, required=False):
        """
        It takes a file path, a list of strings, and a boolean as arguments. It opens the file, reads the
        lines, and inserts the strings at the appropriate place in the file
        
        :param path: the path to the file you want to modify
        :param li: a list of strings and lists
        :param required: True, defaults to False (optional)
        """

        name = li[0]
        str = ""
        str += li[1]
        f = open(path, "r+")
        flag = 0
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip() == (name + ":"):
                print("set flag")
                flag = 1
                index = i
            if flag==1 and line.strip().startswith("required_slots:") and required:
                print("catch")
                index = i + 1
        lines.insert(index, str)
        f.seek(0)
        for line in lines:
            f.write(line)
        print("fichier est modifier "+ name +" !!")



    ## NLU DATA ##########
    ##### ADD Intent
    ###############################################
    ## Fonction pour AJOUTER  dans /data/NLU.yml
    ###############################################

    def add_nluData(name_intent, list_exemple, head=False):
        """
        It adds the header to the nlu data.
        
        :param name_intent: the name of the intent
        :param list_exemple: a list of examples
        :param head: If True, the function will return the header of the nlu data file, defaults to False
        (optional)
        :return: A string
        """
        
        if  head:
            str = 'version: "3.0"\nnlu:'
        else:
            str = ""
        str += "\n- intent: " + name_intent +"\n" + "  examples: |\n"
        for n in range(len(list_exemple)):
            str += "    - " + list_exemple[n] + "\n"
        return str



    ## Config
    ##### Alter Config FILE
    #############################################
    ## Fonction pour MODIFIER le fichier config
    #############################################

    def conf_file(path, language='fr', policies=False):
        """
        It takes a file path, a language, and a boolean as arguments. It opens the file, reads the lines,
        and then replaces the line that starts with "language" with the language argument.
        
        :param path: This is the location of the file, for example:
        "C:/Users/nom_user/Desktop/test/config.yml"
        :param language: the language you want to use, defaults to fr (optional)
        :param policies: if you want to add predefined policies, defaults to False (optional)
        """

        name = language
        f = open(path, "r+")
        lines = f.readlines()
        f.seek(0)
        data = f.read()
        for line in lines:
            if line.split(':')[0] == ("language"):
                data = data.replace(line, 'language: ' + name + "\n")
        f.seek(0)
        f.write(data)
        f.close()
        print("fichier est modifier "+ name +" !!")
        if policies:
            add_file(path, STR_Policy)


    ## Action
    ##### Create and Save Action FILE
    #############################################
    ## Fonction pour creer le fichier Action
    #############################################
    def pickle_action(path):
        """
        It reads the contents of a file, then writes the contents of that file to a pickle file.
        
        :param path: The path to the file you want to pickle
        """

        f = open(path, 'r')
        data = f.read()
        f.close()
        pickle.dump(data, open('test.pkl', 'wb'))

    def Action_file(path, filename="test.pkl"):
        """
        It takes a path and a filename, opens the file, loads the data, and writes the data to the path
        
        :param path: This is the location of the file, for example:
        "C:/Users/nom_user/Desktop/test/config.yml"
        :param filename: the name of the file you want to save the model to, defaults to test.pkl
        (optional)
        """

        f = open(path, 'w')
        infile = open(filename,'rb')
        data = pickle.load(infile, encoding='latin1')
        f.write(data)
        f.close()