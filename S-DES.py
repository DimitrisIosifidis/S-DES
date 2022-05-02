#################################################################
### This is an algorith about Simple-DES ---------------------###
### The functions that supports are:     ---------------------###
###         1) encrypt a message         ---------------------###
###         2) decrypt a message         ---------------------###
###         3) bruteforce to find any key --------------------###
###         that is compatible to decrypt the cipher text ----###
###         4) example option that does all the above --------###
### ----------------------------------------------------------###
### ---This program was written by Iosifidis Dimitrios -------###   
#################################################################

import random
import pyautogui
import timeit

#------------------------------------------------------------#
#------------------- Converting part ------------------------#
#------------------------------------------------------------#

# Converting a string into a list
def Convert_String_to_List(string):
    list1=[]
    list1[:0]=string
    return list1


# Convert a list into a string
def Convert_List_to_String(list):
    # initialize an empty string
    str1 = "" 

    # return string  
    return (str1.join(list))



#------------------------------------------------------------#
#------------------- Checking Values Part -------------------#
#------------------------------------------------------------#



# This functions checks if the input of the user's values is decimal or binary.
def check_Bin_Dec(num):
    
    # set function convert string into set of characters. 
    p = set(num) 
  
    # declare set of '0', '1' . 
    s = {'0', '1'} 
  
    # check set p is same as set s 
    # or set p contains only '0' 
    # or set p contains only '1' 
    # or not, if any one condition 
    # is true then string is accepted 
    # otherwise not. 
    if s == p or p == {'0'} or p == {'1'}: 
        flag = 'Yes' 
    else : 
        flag = 'No'

    return flag




def check_values(key,message):
    

    #-------- Checking the key part --------#

    # Checks if the value is decimal or binary 
    flag_key = check_Bin_Dec(key)

    # Checks if the value is bigger than 10 
    if flag_key == 'Yes' and  len(key) > 10:
        print("We cut your KEY because it is bigger than 10 bits")
        key = key[:10]
       
 

    
    if flag_key == 'No':
        key = int(key)
        key = int(bin(key)[2:])
        key = str(key)

        if len(key) > 10:
            print("We cut your MESSAGE because it is bigger than 8 bits")
            key = key[:10]
        


    # Adds zeros in case that the input is less than 10 
    while len(key) < 10:
        key = str(key).zfill(len(key)+1)



    # -------- Checking the message part --------#

    # Checks if the value is decimal or binary
    flag_msg = check_Bin_Dec(message)   

    # Check if the value is bigger than 8 
    if flag_msg == 'Yes' and  len(message) > 8:
        print("We cut your KEY because it is bigger than 10 bits")
        message = message[:8]


    if flag_msg == 'No':
        message = int(message)
        message = int(bin(message)[2:])
        message = str(message)

        if len(message) > 8:
            print("We cut your MESSAGE because it is bigger than 8 bits")
            message = message[:8]


    # Adds zeros in case that the input is less than 8 
    while len(message) < 8:
        message = str(message).zfill(len(message)+1)
    


    return str(key), str(message)



#------------------------------------------------------------#
#---------------------- S-Des Part --------------------------#
#------------------------------------------------------------#


# P10 Shuffle function
def P10(key_list):
    
    shuffle = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5] 
    key = []
    
    for x in range(10):
        key.insert(x, key_list[shuffle[x]])

    return key
    


# Left shift by one 
def LS_1(key_list):
    left_key = []
    right_key = []

    
    for x in range(5):
        left_key.insert(x,key_list[x])
        right_key.insert(x,key_list[x+5])
    
    

    # Doing the left shift on the left key
    c = left_key[0]
    left_key.remove(left_key[0])
    left_key.insert(4,c)

    

    # Doing the left shift on the left key
    c = right_key[0]
    right_key.remove(right_key[0])
    right_key.insert(4,c)


    return left_key,right_key


# Left shift by two 
def LS_2(left_key,right_key):
    
    c1 = left_key[0]
    c2 = left_key[1]
    left_key.remove(left_key[0])
    left_key.remove(left_key[0])
    left_key.insert(3,c1)
    left_key.insert(4,c2)



    c1 = right_key[0]
    c2 = right_key[1]
    right_key.remove(right_key[0])
    right_key.remove(right_key[0])

    right_key.insert(3,c1)
    right_key.insert(4,c2)

 
    return left_key,right_key


# P8 shuffle function 
def P8(key):
    shuffle = [5, 2, 6, 3, 7, 4, 9, 8]
    
    k1_key = ""

    for x in range(8):
        k1_key+=key[shuffle[x]]

    k1_key = Convert_String_to_List(k1_key)
    return k1_key



# IP shuffle function 
def IP(message_list):
    left_msg = []
    right_msg = []
    
    shuffle = [1, 5, 2, 0, 3, 7, 4, 6]

    modified_message = ""


    for x in range(4):
        left_msg.insert(x,message_list[x])
        right_msg.insert(x,message_list[x+4])


    for x in range(8):
        modified_message+=message_list[shuffle[x]]


    modified_message = Convert_String_to_List(modified_message)
    

    for x in range(4):
        left_msg[x] = modified_message[x]
        right_msg[x] = modified_message[x+4]

    return modified_message, left_msg, right_msg



# Reverse IP function process
def reverse_IP(message):
    
    shuffle = [1, 5, 2, 0, 3, 7, 4, 6]
    reverse_msg = ['0', '0', '0', '0', '0', '0', '0', '0']

    
    for x in range(8):
        reverse_msg.pop(shuffle[x])
        reverse_msg.insert(shuffle[x], message[x])

    return reverse_msg



# EP shuffle function
def EP(right_msg):

    right_msg_str = []

    for x in range(4):
        right_msg_str.insert(x,str(right_msg[x]))

    shuffle = [3, 0, 1, 2, 1, 2, 3, 0]
    mod_right_msg = ""


    for x in range(8):
        mod_right_msg+=right_msg[shuffle[x]]

    mod_right_msg = Convert_String_to_List(mod_right_msg)
 

    return mod_right_msg



# 8 bit XOR 
def XOR_8bit(ep_message,k_key):
    xor_message = []


    for x in range(8):
        if k_key[x] == '0' and ep_message[x] == '0':  
            xor_message.insert(x,str(0))
        elif k_key[x] == '0' and ep_message[x] == '1':
            xor_message.insert(x,str(1))
        elif k_key[x] == '1' and ep_message[x] == '0':
            xor_message.insert(x,str(1))
        elif k_key[x] == '1' and ep_message[x] == '1':
            xor_message.insert(x,str(0))
    
    
    xor_left_msg = []
    xor_right_msg = [] 


    for x in range(4):
        xor_left_msg.insert(x,xor_message[x])
        xor_right_msg.insert(x,xor_message[x+4])
    
    


    return xor_message, xor_left_msg, xor_right_msg




# 4 bit XOR
def XOR_4bit(left_half,right_half):
    SW_list = []

    for x in range(4):
        if left_half[x] == '0' and right_half[x] == '0':
            SW_list.insert(x,0)
        elif left_half[x] == '0' and right_half[x] == '1':
            SW_list.insert(x,1)
        elif left_half[x] == '1' and right_half[x] == '0':
            SW_list.insert(x,1)
        else:
            SW_list.insert(x,0)


    SW_list_str = []
    for x in range(4):
        SW_list_str.insert(x,str(SW_list[x]))
   
    return SW_list_str




# P4 shuffle function
def P4(S_values, left_message):

    S_values_list = Convert_String_to_List(str(S_values))

    shuffle = [1, 3, 2, 0]
    bin_values_list = ""

    for x in range(4):
        bin_values_list+=S_values_list[shuffle[x]]


    bin_values_list = Convert_String_to_List(bin_values_list)

    xor_4bit_msg = XOR_4bit(bin_values_list,left_message)

   
    return xor_4bit_msg
   



# SW shuffle function
def SW_function(message):
    shuffle = [4, 5, 6, 7, 0, 1, 2, 3]
    SW = ""

    for x in range(8):
        SW += message[shuffle[x]]

    SW = Convert_String_to_List(SW)

    
    return SW




# S_function that extracts values from S0 and S1 tables
def S_functions(xor_left_msg, xor_right_msg):     
    
    # Creating the S0 and S1 tables
    S0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]

    S1 = [
        [0, 1, 2, 3], 
        [2, 0, 1, 3], 
        [3, 0, 1, 0], 
        [2, 1, 0, 3]
    ]



    # Getting the decimal values for the S0 table (first and last value)
    if xor_left_msg[0] == '0' and xor_left_msg[3] == '0':
        first_last_dec_S0 = 0 
    elif xor_left_msg[0] == '0' and xor_left_msg[3] == '1':
        first_last_dec_S0 = 1
    elif xor_left_msg[0] == '1' and xor_left_msg[3] == '0':
        first_last_dec_S0 = 2
    else:
        first_last_dec_S0 = 3



    # Getting the decimal values for the S0 table (second and third value)
    if xor_left_msg[1] == '0' and xor_left_msg[2] == '0':
        sec_third_dec_S0 = 0
    elif xor_left_msg[1] == '0' and xor_left_msg[2] == '1':
        sec_third_dec_S0 = 1
    elif xor_left_msg[1] == '1' and xor_left_msg[2] == '0':
        sec_third_dec_S0 = 2
    else:
        sec_third_dec_S0 = 3
        


    # Getting the decimal values for the S1 table (first and last value)
    if xor_right_msg[0] == '0' and xor_right_msg[3] == '0':
        first_last_dec_S1 = 0 
    elif xor_right_msg[0] == '0' and xor_right_msg[3] == '1':
        first_last_dec_S1 = 1
    elif xor_right_msg[0] == '1' and xor_right_msg[3] == '0':
        first_last_dec_S1 = 2
    else:
        first_last_dec_S1 = 3


    # Getting the decimal values for the S1 table (second and third value)
    if xor_right_msg[1] == '0' and xor_right_msg[2] == '0':
        sec_third_dec_S1 = 0
    elif xor_right_msg[1] == '0' and xor_right_msg[2] == '1':
        sec_third_dec_S1 = 1
    elif xor_right_msg[1] == '1' and xor_right_msg[2] == '0':
        sec_third_dec_S1 = 2
    else:
        sec_third_dec_S1 = 3


    # S0_dec_values and S1_dec_values have the decimal values from the table
    S0_dec_values = S0[first_last_dec_S0][sec_third_dec_S0]
    S1_dec_values = S1[first_last_dec_S1][sec_third_dec_S1]


    # Now we make them binary again so to continue with the P4 function.    
    if S0_dec_values == 0:
        S0_bin_values = '00'
    elif S0_dec_values == 1:
        S0_bin_values = '01'
    elif S0_dec_values == 2:
        S0_bin_values = '10'
    else:
        S0_bin_values = '11'

    if S1_dec_values == 0:
        S1_bin_values = '00'
    elif S1_dec_values == 1:
        S1_bin_values = '01'
    elif S1_dec_values == 2:
        S1_bin_values = '10'
    else:
        S1_bin_values = '11'


    return S0_bin_values, S1_bin_values




    


# des_round does the symmetric encryption 
def des_round(message, key, left_msg, right_msg):

    ep_message = EP(right_msg)
    xor_message_key, xor_left_msg, xor_right_msg = XOR_8bit(ep_message,key)
    S0_bin_values, S1_bin_values = S_functions(xor_left_msg, xor_right_msg)
    xor_4bit_msg = P4(S0_bin_values+S1_bin_values,left_msg)
    
    return xor_4bit_msg+right_msg




# Encrypt message with the given key
def encrypt(key,message):
    
    # Finding the K1 and K2
    key_list = Convert_String_to_List(key)
    key_list = P10(key_list)
    left_key, right_key = LS_1(key_list)
    k1_key = P8(left_key+right_key)
    left_key_by_sh2, right_key_by_sh2 = LS_2(left_key,right_key)
    k2_key = P8(left_key_by_sh2+right_key_by_sh2)
    

    message_list = Convert_String_to_List(message)
    modified_message, left_msg, right_msg = IP(message_list)
    
    # Finding the encrypted message
    SW_msg = SW_function( des_round(modified_message, k1_key, left_msg, right_msg) )

    left_msg_SW = []
    right_msg_SW = []

    for x in range(4):
        left_msg_SW.insert(x,SW_msg[x])
        right_msg_SW.insert(x,SW_msg[x+4])

    
    encrypted = reverse_IP( des_round(SW_msg, k2_key, left_msg_SW, right_msg_SW) )
 
    return encrypted 




def decrypt(key,message):
    
    # Finding the K1 and K2
    key_list = Convert_String_to_List(key)
    key_list = P10(key_list)
    left_key, right_key = LS_1(key_list)
    k1_key = P8(left_key+right_key)
    left_key_by_sh2, right_key_by_sh2 = LS_2(left_key,right_key)
    k2_key = P8(left_key_by_sh2+right_key_by_sh2)
 

    message_list = Convert_String_to_List(message)
    modified_message, left_msg, right_msg = IP(message_list)
    

    # Finding the decrypted message
    SW_msg = SW_function( des_round(modified_message,k2_key,left_msg,right_msg) )

    left_msg_SW = []
    right_msg_SW = []

    for x in range(4):
        left_msg_SW.insert(x,SW_msg[x])
        right_msg_SW.insert(x,SW_msg[x+4])

    decrypted = reverse_IP(des_round(SW_msg,k1_key,left_msg_SW,right_msg_SW))

    return decrypted 




#------------------------------------------------------------#
#-------------------- Brute-force Part ----------------------#
#------------------------------------------------------------#

def bruteforce_attack(message, cipher):
    # We set the character that we want to generate
    character = "01"
    character_list = list(character)
    y = pow(2,10)+1


    # Starts Timer
    start = timeit.default_timer()

    
    # Starts the guessing process
    guess_key = ''
    all_keys = []
    keys = []
    counter = 0

    for x in range(y):
        guess_key = random.choices(character_list, k=len(cipher)+2)
            
        if cipher == encrypt(guess_key, message):
            all_keys.insert(counter, guess_key)
            counter+=1

    # Using list comprehension to remove duplicated from list 
    [keys.append(x) for x in all_keys if x not in keys]

    # Print all the possible keys
    for x in range(len(keys)):
        print("Key that is valid:", keys[x])


    # Stop Timer
    stop = timeit.default_timer()
    time = stop - start
    
    print("Time for the Bruteforce Attack:",str(time)[:5],"seconds")




# Print all the modes that user can use.
def printHelp():
    
    print("Modes:")
    print("--example")
    print("--encrypt")
    print("--decrypt")
    print("--bruteforce")

    print("/------------------------------------/")
    answer = input()
    
    while answer!='--example' and answer!='--encrypt' and answer!='--decrypt' and answer!='--bruteforce':
        print("------------------------------------")
        
        print("Give the correct mode!")
        print("--example")
        print("--encrypt")
        print("--decrypt")
        print("--bruteforce")
        
        print("/------------------------------------/")
        answer = input()
    
    print("/------------------------------------/")

    return answer 




def example():
    key = '0101101000'
    message = '00010101'
    print("KEY:",key," MESSAGE:", message)

    encrypted = encrypt(key,message)
    print("Encrypted message is:",encrypted)

    decrypted = decrypt(key,encrypted)
    print("Decrypted message is:",decrypted)

    print("/------------------------------------/")
    print("Starting the bruteforce attack...")
    bruteforce_attack(message, encrypted)

    

#--------------------------------------------------------#
#---------------------- Main Part -----------------------#
#--------------------------------------------------------#


answer = printHelp()
if answer == "--example":
    example()

elif answer == "--encrypt":

    key = input("Give the key:")
    message = input("Give the message:")
    key , message = check_values(key,message)
        
    encrypted = encrypt(key,message)
    print("Encrypted message is:", encrypted)
 
elif answer == "--decrypt":
    key = input("Give the key:")
    message = input("Give the message:")
    key , message = check_values(key,message)

    decrypted = decrypt(key,message)
    print("Decrypted message is:", decrypted)

elif answer == "--bruteforce":
    cipher = input("Give the cipher text:")
    message = input("Give the message:")
    
    cipher = Convert_String_to_List(cipher)

    print("Starting the bruteforce attack...")
    bruteforce_attack(message, cipher)
