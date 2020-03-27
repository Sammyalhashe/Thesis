# Schedule for thesis
### Student: Sammy Al Hashemi
### Supervisor: Glenn Gulak

#### Six week sprint:
Here, we get done a majority of the project before midterms. It comprises of several parts. 

-   September 25 - October 5
    - Reproduce the results of Yusef's code
    - finish lit review on previous Grover's implementations
    - Shortet vector problem (SVP): know way to solve it -> grovers on qunatum computer
        - known sub-exponential time method
    - We may not be intersted in grovers for a general database overview -> more interested in sorting
    - read every important paper that comments on Grover's oracle -p> practical version of an oracle for Grovers
-   October 6 - October 15
    - build someone's practical version of oracle -> be skeptical and build it before you move forward
    - need to get a firmhold on someone's working oracle before midterms
    - After reproducing results of Grover's algorithm from Yusef's thesis, attempt to parameterize the code to introduce some faction of scalability.
        - The algorithm reproduced in Yusef's thesis is only a demonstration of Grover's algorithm, where the target state is known before construcitng the compiled circuit. 
        - In order to be useful, the target must be unknown, even after the compilation of the circuit.
    - Analyze this new paramaterization for its time complexity. Does it cause any significant changes?
    - Begin documenting steps taken in primary thesis report.
- October 16 - November 16
    - This is the step where the oracle of the algorithm has to be considered. 
    - what components deterimine overall performance -  where does all the time go?
    - after, focus engineering effort on those components
    - parameterizing what other people have done
            - Look into reproducing the algorithm without an oracle function.

Build it and understand what the hell is going on and also maybe notice somethign along the lines of  "this can be imporoved" and maybe improve by x percent.

Quantum Zoo -> check out this website
