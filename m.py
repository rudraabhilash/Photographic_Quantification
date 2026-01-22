

# a =  [634,346536,43634353,3435534,53635] #len(a) = 1000
# exposure = 653654333                      

# #case 1: DP approach: O(len(a)*exposure)
# f(idx,s) = f(idx-1,s-a[i]) or f(idx-1,s)

# #Only indexOfLastElement * exposure many unique function calls can exist
# def f(indexOfLAstElement, exposure):
#     if exposure == 0:
#         return True
#     if indexOfLAstElement < 0:
#         return False
#     include = f(indexOfLAstElement-1, exposure-a[indexOfLAstElement])
#     exclude = f(indexOfLAstElement-1, exposure)
#     return include or exclude



import pandas as pd
df1 = pd.DataFrame({'Obligors': ['Ob1', 'Ob2'],
                    'losses':[234,3453],
                    'id':[1,2]
                    })
df2 = pd.DataFrame({'sectors': ['Tech', 'Semicon'],
                    'exposure': [534345,353453],
                    'id':[1,2]
                    })
ans = df1.merge(df2, on = "id")
ans = ans.drop_duplicates(subset=['sectors'])
print(ans)

yours_occupied = [ [9,10], 
                   [11,12],
                   [14,15],
                   [16,17]]
mine_occupied = [
                    [8,10], 
                    [10,11],
                    [13, 14],
                    [14,16]]

key - (start,end)
value - True

#common free time

       8    9  10   11    12   13     14    15     16   17
---------------------------------------------------------
