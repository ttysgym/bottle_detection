# -*- coding: utf-8 -*-

def translate_language(lang, scene, debug=False):
    """
    Language translation dictionary
    -------------
    init_dict keys

    k = Kinyarwanda
    e = English
    f = French
    j = Japanese
    -------------
    Available scene list on 2020_10_19
    
    l_select0
    l_select1
    l_select2
    l_select3
    select4
    m_select0
    m_select1
    m_select2
    m_select3
    current
    status
    choice
    mode
    mode_select
    setup_mode
    setup_choice
    welcome
    scan_start
    read_message
    time
    correct?
    continue?
    cancel
    total
    subtotal
    can_not_read
    input_error
    thanks
    next
    -------------
    'debug' initial setting is False.
    If you give True, it checks the length of each dictionary and compare to key types,
    returns the result
    """

    init_dict = {
    "k" : {"l_select0" : '\n----------Uburyo bwo guhitamo ururimi----------',
         "l_select1" : 'Nyamuneka hitamo ururimi : ',
         "l_select2" : "\nIgenamiterere ry'ururimi ryarangiye : {}",
         "l_select3" : "\nGusohoka mu guhitamo ururimi?\nInjira 'y' cyangwa 'n' : ",
         "select4" : "\nNyamuneka andika inyuguti zukuri. : ",
         "m_select0" : '\n----------Uburyo bwo gusesengura uburyo bwo guhitamo uburyo----------',
         "m_select1" : 'Nyamuneka hitamo icyitegererezo : ',
         "m_select2" : "\nIgenamiterere ry'icyitegererezo ryarangiye : {}",
         "m_select3" : "\nGusohoka muburyo bwo guhitamo?\nInjira 'y' cyangwa 'n' : ",

         "current" : "\n----------Imiterere y'ubu---------",
         "status" : "icyitegererezo : {}\nururimi : {}",
         "choice" : "\n----------Nyamuneka hitamo uburyo bwo gutangira----------",
         "mode" : "1 : Tangira muburyo bwo kwandikisha amafaranga\n2 : Tangira muburyo bwo gushiraho\n3 : Tangira muburyo bw'ishusho",
         "mode_select" : "Nyamuneka hitamo wandike umubare : ",

         "setup_mode" : "\n----------Uburyo bwo gushiraho----------",
         "setup_choice" : "Ni ubuhe buryo bwo gushiraho?\n1 : Gushiraho icyitegererezo\n2 : Gushiraho ururimi\n3 : Garuka kubibanjirije\n Iyinjiza : ",

         "welcome" : 'murakaza neza!', 
         "scan_start" : 'Gusikana ibicuruzwa, shyira mumwanya wifuza hanyuma ukande "Enter".',
         "read_message" : 'Ibicuruzwa bikurikira byarasomwe.',
         "time" : '{}[s] yararenganye kugeza igihe ikintu gisomwe.',
         "correct?" : 'Kanda "y" niba ibicuruzwa byasomwe aribyo, cyangwa ukande "n" niba atari byo. : ',
         "continue?" : 'Kanda "y" kugirango ukomeze gusikana ibintu byose, "f" kugirango urebe, cyangwa "x" niba ufite ibintu byo guhagarika. : ',
         "cancel" : 'Injiza umubare wibicuruzwa ushaka guhagarika. : ',
         "total" : 'Igiciro-cyose: {}',
         "subtotal" : 'Subtotal : {}',
         "can_not_read" : 'Ntabwo yasomye neza. Nyamuneka usubize ikintu mumwanya wabigenewe.',
         "input_error" : 'Nyamuneka andika neza',
         "thanks" : 'Urakoze kugura!',
         "next" : 'Nyamuneka shyira ikintu gikurikira mumwanya wagenwe',
         "delete" : 'Injira ikintu ushaka gusiba numubare kuva 0 kugeza {}, kanda "n" niba udashaka gusiba',
         "delete_complete" : 'Ibintu bikurikira byasibwe',
         "not_registered" : 'Ibicuruzwa byiyandikishije ntibishobora kumenyekana'
         },

    "e" : {"l_select0" : '\n----------Language select mode----------',
         "l_select1" : 'Please select the language : ',
         "l_select2" : '\nLanguage setting completed : {}',
         "l_select3" : "\nExit language select mode?\nEnter 'y' or 'n' : ",
         "select4" : "\nPlease enter the correct characters : ",
         "m_select0" : '\n----------Analytical model select mode----------',
         "m_select1" : 'Please select the model : ',
         "m_select2" : '\nModel setting completed : {}',
         "m_select3" : "\nExit model select mode?\nEnter 'y' or 'n' : ",

         "current" : "\n----------Current status---------",
         "status" : "model : {}\nlanguage : {}",
         "choice" : "\n----------Please choice start up mode----------",
         "mode" : "1 : Start in cash register mode\n2 : Start in set up mode\n3 : Start in image mode",
         "mode_select" : "Please select and enter the number : ",

         "setup_mode" : "\n----------Setting mode----------",
         "setup_choice" : "Which setting mode?\n1 : Model setting\n2 : Language setting\n3 : Return to the previous\n input : ",


         "welcome" : 'welcome!', 
         "scan_start" : 'To scan the product, place it in the desired position and press "Enter".',
         "read_message" : 'The following products have been read.',
         "time" : '{}[s] has passed until the item is read.',
         "correct?" : 'Press "y" if the read product is correct, or press "n" if it is incorrect. : ',
         "continue?" : 'Press "y" to continue scanning any items, "f" to check out, or "x" if you have items to cancel. : ',
         "cancel" : 'Enter the number of the product you want to cancel. : ',
         "total" : 'Total-Price: {}',
         "subtotal" : 'Subtotal : {}',
         "can_not_read" : 'It did not read correctly. Please reposition the item in the designated position.',
         "input_error" : 'Please input correctly',
         "thanks" : 'Thank you for buying!',
         "next" : 'Please put the next item in the specified position.',
         "delete" : 'Enter the item you want to delete with a number from 0 to {}, press "n" if you do not want to delete.',
         "delete_complete" : 'The following items have been deleted.',
         "not_registered" : 'Registered products could not be detected.'
         },

    "f" : {"l_select0" : "\n----------Mode de sélection de la langue----------",
         "l_select1" : 'Veuillez sélectionner la langue : ',
         "l_select2" : '\nRéglage de la langue terminé : {}',
         "l_select3" : "\nQuitter le mode de sélection de la langue?\nEntrez 'y' ou 'n' : ",
         "select4" : "\nVeuillez saisir les caractères corrects. : ",
         "m_select0" : '\n----------Mode de sélection du modèle analytique----------',
         "m_select1" : 'Veuillez sélectionner le modèle : ',
         "m_select2" : '\nConfiguration du modèle terminée : {}',
         "m_select3" : "\nQuitter le mode de sélection de la modèle?\nEntrez 'y' ou 'n' :",

         "current" : "\n----------Statut actuel---------",
         "status" : "modèle : {}\nlangue : {}",
         "choice" : "\n----------Veuillez choisir le mode de démarrage----------",
         "mode" : "1 : Démarrer en mode caisse enregistreuse\n2 : Démarrer en mode configuration\n3 : Démarrer en mode image",
         "mode_select" : "Veuillez sélectionner et saisir le numéro : ",

         "setup_mode" : "\n----------Mode de réglage----------",
         "setup_choice" : "Quel mode de réglage?\n1 : Réglage du modèle\n2 : Paramètres de langue\n3 : Revenir au précédent\n contribution : ",

         "welcome" : 'bienvenu!', 
         "scan_start" : 'Pour numériser le produit, placez-le dans la position souhaitée et appuyez sur «Entrée».',
         "read_message" : 'Les produits suivants ont été lus.',
         "time" : "{}[s] est passé jusqu'à ce que l'élément soit lu.",
         "correct?" : "Appuyez sur 'y' si le produit lu est correct, ou appuyez sur 'n' s'il est incorrect. : ",
         "continue?" : "Appuyez sur 'y' pour continuer la numérisation des éléments, sur 'f' pour vérifier ou sur 'x' si vous avez des éléments à annuler. : ",
         "cancel" : 'Saisissez le numéro du produit que vous souhaitez annuler.: ',
         "total" : 'Prix-total: {}',
         "subtotal" : 'Sous-total : {}',
         "can_not_read" : "Il n'a pas lu correctement. Veuillez repositionner l'élément dans la position désignée.",
         "input_error" : 'Veuillez saisir correctement',
         "thanks" : "Merci d'avoir acheté!",
         "next" : "Veuillez mettre l'élément suivant dans la position spécifiée",
         "delete" : "Entrez l'élément que vous souhaitez effacer avec un nombre compris entre 0 et {}, appuyez sur 'n' si vous ne souhaitez pas effacer",
         "delete_complete" : "Les éléments suivants ont été supprimés",
         "not_registered" : "Les produits enregistrés n'ont pas pu être détectés"
         },

    "j" : {"l_select0" : '\n----------言語選択モード----------',
         "l_select1" : '言語を選択してください。 : ',
         "l_select2" : '\n言語設定が完了しました : {}',
         "l_select3" : "\n言語選択モードを終了しますか？\n'y'->終了　 'n'->もう一度選択 : ",
         "select4" : "\n正しい文字を入力してください。 : ",
         "m_select0" : "\n----------分析モデル選択モード---------- : ",
         "m_select1" : 'モデルを選択してください。 : ',
         "m_select2" : '\nモデル設定が完了しました : {}',
         "m_select3" : "\nモデル選択モードを終了しますか？\n'y'->終了　 'n'->もう一度選択 : ",

         "current" : "\n----------現在のステータス---------",
         "status" : "モデル : {}\n言語 : {}",
         "choice" : "\n----------起動モードを選択してください----------",
         "mode" : "1 : レジモード\n2 : セットアップモード\n3 : 撮影モード",
         "mode_select" : "数字を入力してください : ",

         "setup_mode" : "\n----------セットアップモード----------",
         "setup_choice" : "どの設定を変更しますか？\n1 : モデル設定\n2 : 言語設定\n3 : 前の画面に戻る\n 数字を入力してください : ",

         "welcome" : 'いらっしゃいませ!', 
         "scan_start" : 'スキャンする場合は商品を指定の位置に置いて「Enter」を押して下さい。',
         "read_message" : '読み取られた商品の一覧は以下になります。',
         "time" : '商品を読み取るまで {}[s] 経過しました。',
         "correct?" : '読み取られた商品が正しい場合は「y」、誤っている場合は「n」を押してください。 : ',
         "continue?" : '続けて商品をスキャンする場合は「y」、会計する場合は「f」、\n キャンセルする商品がある場合は「ｘ」を押して下さい。 : ',
         "subtotal" : '小計 : {}',
         "total" : '合計 : {}',
         "can_not_read" : '正しく読み取れませんでした。商品を指定の位置に置き直してください。',
         "input_error" : '正しく入力されていません。',
         "thanks" : 'ご利用ありがとうございました！',
         "next" : '次の商品を指定の位置に置いてください。',
         "delete" : '消去したい商品を 0 から {} の番号で入力してください, 消去しない場合は「n」を押してください : ',
         "delete_complete" : '以下の商品を消去しました',
         "not_registered" : '登録商品を検出できませんでした'
         }
    }
    
    # Enable if you want to debug
    # Check the length of each dictionary
    if debug:
        lang_list = ["k", "e", "f", "j"]
        # length
        kin = len(init_dict["k"])
        eng = len(init_dict["e"])
        fra = len(init_dict["f"])
        jpn = len(init_dict["j"])

        # keys
        kin_keys = list(init_dict["k"].keys())
        eng_keys = list(init_dict["e"].keys())
        fra_keys = list(init_dict["f"].keys())
        jpn_keys = list(init_dict["j"].keys())
        check_list = [kin_keys, eng_keys, fra_keys, jpn_keys]
        
        key_all = kin_keys + eng_keys + fra_keys + jpn_keys
        #print(key_all)
        diff_key = [x for x in set(key_all) if key_all.count(x) == len(lang_list)]
        if diff_key:
          print("KeyError : There is a key that is different from other lists.")

        for i, l in enumerate(check_list):
          diff = set(key_all) ^ set(l)
          if diff:
              print("{} : {}".format(lang_list[i], diff))

        if kin == eng == fra == jpn and not diff:
          pass
        elif kin == eng == fra == jpn and diff:
          print("\n Please　make sure the key type is the same")
          return
        else:
          print("LengthError : Some sentences can't be translated because the length of the dictionary is different.")
          print("---------")
          print("the length of each dict\n kin: {}, eng: {}, fra: {}, jpn: {}".format(kin, eng, fra, jpn))
          return


    #print(lang_dict)
    lang_dict = init_dict[lang]
    #print(tmp)
    sentense = lang_dict[scene]

    return sentense
