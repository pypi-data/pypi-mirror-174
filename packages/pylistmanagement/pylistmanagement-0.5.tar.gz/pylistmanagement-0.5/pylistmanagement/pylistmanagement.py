class pylistmanagement:
    def impute(self,list1,method="zero"):
        if len(list1)==0:
            return(print("This list is empty"))

        n_miss = list1.isnull().sum()
        perc = n_miss / len(list1) * 100
        if method=="zero":
            lista_new=list1.fillna(0)
        elif method == "mean":
            lista_new=list1.fillna(int(list1.mean()))
        elif method == "median":
            lista_new=list1.fillna(int(list1.median()))

        print("A total of ",n_miss," null values have been deleted. ",int(perc),"%")
        return lista_new

    def column_operation(self,listas,method="concat"):
        try:

            for m in listas:
                if len(m)==0:
                    return(print("Some lists may be empty"))
            for m in range(len(listas)):
                if len(listas[m])!=len(listas[1]):
                    return(print("The length of the lists must always be the same."))
            
            if method=="add":
                try:
                    lista_new= listas[0] + listas[1]
                    if len(listas) > 2:
                        for k in range(2,len(listas)):
                            lista_new = lista_new + listas[k]
                except:
                    return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! All the lists must contain int or float values\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))

            elif method=="subtract":
                try:
                    lista_new= listas[0] + listas[1]
                    if len(listas) > 2:
                        for k in range(2,len(listas)):
                            lista_new = lista_new + listas[k]
                except:
                    return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! All the lists must contain int or float values\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))


            elif method=="concat":
                lista_new = ['' for i in range(len(listas[0]))]
                for l in range(len(listas[0])):
                    for lista in listas:
                        lista_new[l] += str(lista[l])
            else:
                return(print("Select a valid method"))
            return lista_new
        except:
            return print("Remember to add the parameters correctly")

    def filtering(self,dataf,list1,filter,method ="equal"):
        if method == "equal":    
            new_dataf = dataf[dataf[list1]==filter]
            return new_dataf

        elif method == "higher":    
            try: 
                new_dataf = dataf[dataf[list1]>filter]
                return new_dataf
            except:
                return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! The filter should be a number\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))

        elif method == "equal_higher":    
            try:
                new_dataf = dataf[dataf[list1]>=filter]
                return new_dataf
            except:
                return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! The filter should be a number\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))

        elif method == "lower":    
            try:
                new_dataf = dataf[dataf[list1]<filter]
                return new_dataf
            except:
                return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! The filter should be a number\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))

        elif method == "equal_lower":    
            try:
                new_dataf = dataf[dataf[list1]<=filter]
                return new_dataf
            except:
                return(print("\n!!!!!!!!!!!!!!!!!!!!!!!!\nError has occurred! The filter should be a number\n!!!!!!!!!!!!!!!!!!!!!!!!\n"))
        else:
            return(print("Select a valid method\n"))