#!/bin/python3
#-*-encode: utf-8-*-
#
def __help__(_baner_: bool = True):
    if _baner_:
     #  print("""\n\r
  #  _                               __
  # (_)___ ___  ____ _____ ____     / /_____
  #/ / __ `__ \/ __ `/ __ `/ _ \   / __/ __ \ 
# / / / / / / / /_/ / /_/ /  __/  / /_/ /_/ /
#/_/_/ /_/ /_/\__,_/\__, /\___/   \__/\____/
#                  /____/""")
    #    print("""         ________________
#        / ____/  _/ ____/
#       / / __ / // /_
# _    / /_/ // // __/
#(_)   \____/___/_/          By:__DDr669__""")
        print(""" ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
▕▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░▏
▕▒▒▒(‾)▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒▒▒░░░░▒▒▒▒▒/‾/▒▒▒▒▒▒▒▒░░░░▏
▕▒▒/ / ‾_ `__‾\/‾‾‾ `/‾__‾`/‾_‾\▒▒/  _ /‾__‾\▒░░░░░▏
▕▒/ / /▒/ /▒/ / /▒/ / /▒/ / /__/▒▒/ /▒/ /▒/ /░░░░░░▏
▕/_/_/▒/_/▒/_/\__,_/\_ , /\ __/▒▒▒\__/\_ __/░░░░░░░▏
▕▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░/___/▒▒░░░░▒▒░░░░░░░░░░░░░░░░░░▏
▕▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░▏""")
        print("""▕▒▒▒▒▒▒▒▒/‾_‾_‾/‾‾‾/‾__‾‾/░░░░░░░░░░░░░░░░░░░░░░░░░▏
▕▒▒▒▒▒▒▒/ / __ / // /_░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▏
▕▒▒▒▒▒▒/ /_/ // // __/░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▏
▕(‾)▒▒▒\____/___/_/░░░░░░░░░░░░░By:__DDr669__░░░░░░▏
▕▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▏
 ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔""")
    
    print("usage python3|./transforma_gif.py -p path_to_files -s 2 -f 12 -ext jpeg|jpg|bmp|png -o out_file")
    print("")
    print("\t-p\t|\t--path")
    print("\t-s\t|\t--size\t|\t-q\t|\t--queue")
    print("\t-ext\t|\t--extension")
    print("\t-f\t|\t--framerate")
    print("\t-o\t|\t--out")

#༺
# ― 
# ‾ ⁄ ▰ ▒ ░
def return_file_() -> dict:
    _ = { "extension": None,    #   extenção do arquivo
          "out_ext": ".gif",    #   extenção da saida
          "framerate": 8,       #   framerate da saida
          "size": 2,            #   quantidade de arquivos
          "path": None,
          "out_path": None}        #   caminho dos arquivos
    # ⬊ ☞
    _["path"] = input("Path to find files ☞")
    _["size"] = input("how much images ☞")
    _["out_path"] = input("archive to save ☞")
    return _ 


def cmdline_verify(array: list) -> dict:
    counter = 0
    _ = { "extension": None,    #   extenção do arquivo
          "out_ext": ".gif",    #   extenção da saida
          "framerate": 8,       #   framerate da saida
          "size": 2,            #   quantidade de arquivos
          "path": None,
          "out_path": None}        #   caminho dos arquivos
    for ITEM in array:
        match ITEM:
            case "-avi" | "-AVI":
                try: 
                    _["extension"] = "avi"
                except IndexError as Err:
                    return -1
            case "-ext" | "--extension":
                try: 
                    _["extension"] = array[counter + 1]
                except IndexError as Err:
                    return -1
            case "-f" | "--frame" | "--frame-rate":
                try: 
                    _["framerate"] = array[counter + 1]
                except IndexError as Err:
                    return -1
            case "-s" | "--size" | "-q" | "--quantidade" | "--files":
                try:
                    _["size"] = array[counter + 1]
                except IndexError as Err:
                    return -1    
            case "-p" | "--path":
                try:
                    _["path"] = array[counter + 1]
                except IndexError as Err:
                    return -1 
            case "-o" | "--out":
                try:
                    _["out_path"] = array[counter + 1]
                except IndexError as Err:
                    return -1
                
        if counter < len(array):
            counter += 1
        else:
            return _
    return _

if __name__ == "__main__":
   
    app = __help__()
