# python代码
def calc_sum(a, b):
    return a + b

# lua代码
lua_code = '''
a = "a"
b = "b"
print("Hello World!")
print(a .. b)
'''

# 代码
'''
IF "shou3".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "cc视觉".r_data[#i] = ',' OR "cc视觉".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "cc视觉".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "cc视觉".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    
    "cc视觉".r_data := "cc视觉".e_data;
    
    IF "cc视觉".u_data[0] = 'image' THEN
        "e发送"(buf := 'ok',
              num := 1);
    END_IF;
    
END_IF;
'''