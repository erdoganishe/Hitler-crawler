# Hitler crawler

Brute force - ~1,5 hours:
    
    Non-optimised method which works slowly, but gets correct results
    For this executing time for 3 redirects ~2200s, ~7s for 2 redirects

Brute force optimised ~ + 1 hour: 

    Optimised version of brute force:

        Added Beautiful Soup 4 library for better parse performance
        Changed list to deque(double-edged query). This gets better performance for 3+ redirects. For list we get fixed order for in and out for links, but now it`s random, so for small value of redirects it gets unstable of execution time: from ~2.5s to ~30s, but it has no influence for big values because of substantially growing algoritm complexity. *O*(*b<sup>r+1</sup>*), b for base(avg redirects on wiki page), r for number of redirects in path). 

    For this executing time for 3 redirects ~1200s

