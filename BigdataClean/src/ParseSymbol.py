import re
from ParseData1 import position_tmp

def ParseSymbol(position_tmp):
# 1. filter &#xx;
#        / &#47;
    tmp1 = position_tmp.replace('&#47;','/')
#        ( &#40;
    tmp2 = tmp1.replace('&#40;','(')
#        : &#58;
    tmp3 = tmp2.replace('&#58;',':')
#        ) &#41;
    tmp4 = tmp3.replace('&#41;',')')
#        ' &#39;
    tmp5 = tmp4.replace('&#39;','\'')
#        - &#8211;
    tmp6 = tmp5.replace('&#8211;','-')
#        & &#38;
    tmp7 = tmp6.replace('&#38;','&')
#        ; &#59;
    tmp8 = tmp7.replace('&#59;',';')
#        + &#43;
    tmp9 = tmp8.replace('&#43;','+')
#        \ &#92;
    tmp10 = tmp9.replace('&#92;','\\')
#        @ &#64;
#        It may be the location!!!
    tmp11 = tmp10.replace('&#64;','@')
#        ! &#33;
#        Turn to be null
    tmp12 = tmp11.replace('&#33;','')
#        $ &#36;
    tmp13 = tmp12.replace('&#36;','$')
#        [ &#91;
    tmp14 = tmp13.replace('&#91;','[')
#        ] &#93;
    tmp15 = tmp14.replace('&#93;',']')
#        E &#201;
#        Special Franch character
    tmp16 = tmp15.replace('&#201;','E')
#        / &#65295;
    tmp17 = tmp16.replace('&#65295;','/')
    position_tmp = tmp17
    
# Parse the Ref  
def ParseRef(position_tmp):
    # 2. Keep the symbol of (Refxxx OR [Refxxx
    p_position_filter_symbol = re.compile(r'[\(\[]Ref')
    position_filter_symbol = p_position_filter_symbol.search(position_tmp)
    if position_filter_symbol != None:
        p_position_filter1 = re.compile(r'(.*?)[\(\[]Ref')
        position_filter1 = p_position_filter1.search(position_tmp)
        position_tmp = position_filter1.group(1)
        
# Parse the salary and work duration from the position field
def ParseSalaryDuartion(position_tmp):
    p_content_in_blank = re.compile(r'\((.*?)\)')
    if p_content_in_blank.search(position_tmp) != None:
        content_in_blank = (p_content_in_blank.search(position_tmp)).group(1)
        #print content_in_blank
#        a. parse salary
        p_salary_in_blank = re.compile(r'\$(.*)')
        if p_salary_in_blank.search(content_in_blank) != None:
            salary_tmp = content_in_blank
            #print salary_tmp
        p_salary_in_blank1 = re.compile(r'[0-9]K')
        if p_salary_in_blank1.search(content_in_blank) != None:
            salary_tmp = content_in_blank
            #print salary_tmp
#        b. parse work duration
        p_duration_in_blank = re.compile(r'Day')
        if p_duration_in_blank.search(content_in_blank) != None:
            workduration_tmp = content_in_blank        
