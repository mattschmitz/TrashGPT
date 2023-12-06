# FOR TESTINGIN THONNY ONLY

while True:
    user_input = input("Enter 1 to take a picture, or press Enter to do nothing: ")
    
    try: 
        if user_input == "1":
            
            ## do something here
            
    except Exception as e:
        LoopErrorIndicator()
        print("Exception in Loop")
        print(str(e))
        gc.collect()
        takepic = False #reset
        continue