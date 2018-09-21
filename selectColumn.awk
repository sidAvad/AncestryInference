#Prints column whose header contains 'g3' 

awk  '
        NR==1 {
                printf ("%s\t", $1);
                for (i=1; i<=NF; i++) {
                        if ($i~/g3/) {
                                title=i;
                                print $i;
                        }
                }
        }
        NR>1 {  
                printf ("%s\t", $1);
                if (i=title) {
                        print $i;
                }
        }
' $1

