# canitsynchro
Python constraint solver for Shimano Di2 (or similar) Full Synchronised Shift mapping

## Ussage:

python3 canitsynchro.py"[CHAINRING SMALL/LARGE]" -c "[CASSETTE MODEL / COGS]" [ADDITIONAL OPTIONS]

## Arguments:
  -h, --help    show help
  
  -c 
  Cassette model name OR comma/space separated string of cogs
  
  -min
  Minimum Jump in percent divided by 100 (default: 0.08)
  
  -max
  Maximum Jump in percent divided by 100 (default: 0.16)
  
  -adj
  Adjacent shift tolerance, i.e compare percentual jump to the ones that come before/after (default:
                0.1)
    
  -small
  Number of small cogs to restrict on the small ring (default: 3)
  
  -big
  Number of large cogs to restrict on the big ring (default: 2)

  Example ussage for calculating a 2x11 MTB Setup with the default settings:
  
  ´python3 canitsynchro.py "24/34" -c "11 13 15 17 19 21 24 27 31 35 40"´
  
### Info:
  Valid syntaxes for cassete spacing are:
  - "11, 13, ..."
  - "11 13 ..."

  Extra spaces aswell as duplicates will be ignored (for example typing "11  13 13 15 17 ..." will be treated as "11, 13, 15, 17, ...")



  The valid syntex for cassete models is:

  CS-MXXXX (MTB)
  
  CS-RXXXX (Road)
  
  CS-HGXXX (General purpose HG Cassetes

The Database isnt implemented yet!

  ### Advice for interpreting results
  
  This is personal preference (wich is why you can tune it)
  but generally you want to choose the crossover that:
  - has a gear step close to what comes before and after
  - isn't too big, neither too small
  - happens in the middle of the cassete
  - does not severely bias a certain ring 
  
This tool is meant to save you from creating spreadsheets to calculate the possible crossover, i hope it does so.

### more to come
i am intending on making the tool a little more user friendly in the future by adding a premade list of all the cassetes you may use in a 2x setup
i.e you will be able to type "M9000 11-40" insthead of the cogs themselves.

First i'll be adding shimano, botique makers will follow eventually
