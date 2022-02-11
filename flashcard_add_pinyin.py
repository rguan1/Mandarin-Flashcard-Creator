
import argparse
import cedict_parser
import pinyin_converter
from pinyin_converter import decode_pinyin
import pandas as pd
import re


# create the dictionary
cedict = cedict_parser.simplified_to_pinyin_english()


def characters_to_pinyin(characters):
    #strip [] and ()
    clean_characters = re.sub(r'[(（）)]', '', characters)
    
    #check if phrase is in dictionary
    if clean_characters in cedict:
        return check_multiple_defs(cedict[clean_characters], clean_characters, characters)
    else:
        #phrase not in dictionary so brute force it with original characters
        return characters_to_pinyin_by_each_character(characters)

    
def check_multiple_defs(mdefs, searched_chars, orig_characters):
    all_pinyins_numbered = sorted(list(set(list(map(lambda sdef: sdef.pinyin.lower(), mdefs)))))
    all_pinyins = list(map(lambda p: decode_pinyin(p), all_pinyins_numbered))
    if len(all_pinyins) == 1:
        #only one result so print that
        spinyin = all_pinyins[0]
    else:
        #print all pinyins and all caps tell user to pick

        all_pinyins_str = ", ".join(all_pinyins)

        print("You can use numerical order starting from 1 to indicate choice")
        print(f"For {searched_chars} in '{orig_characters}', which pinyin: {all_pinyins_str}")
        pinyin_choice = all_pinyins[int(input()) - 1]

        spinyin = pinyin_choice
    return spinyin
    
    
def characters_to_pinyin_by_each_character(characters):
    
    pinyin_equivalent = ""
    for schar in characters:
        if schar in cedict:
            spinyin = check_multiple_defs(cedict[schar], schar, characters)
            
            pinyin_equivalent += spinyin
        else:
            # presumably it is a non chinese character
            pinyin_equivalent += schar
            
    return pinyin_equivalent
    

def add_pinyin_to_list(flashcard_f, csv_out):
    #expects characters and english columns during import. 
    flashcards = pd.read_csv(flashcard_f, sep="\t", header=None)
    flashcards.columns = ["characters", "english"]
    flashcards["pinyin"] = flashcards.apply(lambda row: characters_to_pinyin(row.characters), axis = 1)
    flashcards = flashcards.reindex(columns=["english", "characters", "pinyin"])
    flashcards.to_csv(csv_out, sep ='\t', index=False, header=False)
    

def main():
    parser = argparse.ArgumentParser(description='Adds Pinyin to csv/txt files based on chinese characters')
    parser.add_argument('--file-in-path', type=str, help='File path to txt/csv to add Chinese Pinyin to')
    parser.add_argument('--csv-out-path', type=str, help='File path for final csv with pinyin')
    args = parser.parse_args()
    add_pinyin_to_list(args.file_in_path, args.csv_out_path)
    print(f"Completed csv is at {args.csv_out_path}")
    
    
if __name__ == "__main__":
    main()




