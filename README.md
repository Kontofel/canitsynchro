# canitsynchro
Python constraint solver for Shimano Di2 (or similar) Full Synchronised Shift mapping

## Ussage:

python3 canitsynchro.py "[CHAINRING]" -c "[CASSETTE MODEL / COGS]" [ADDITIONAL OPTIONS]

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

  Example with Road 2x12 using the Cassette database:
  ´python3 canitsynchro.py "34/50" -c "CS-R9200 11-34"´
### Info:
  Valid syntaxes for cassete spacing are:
  - "11, 13, ..."
  - "11 13 ..."

  Extra spaces aswell as duplicates will be ignored (for example typing "11  13 13 15 17 ..." will be treated as "11, 13, 15, 17, ...")
  Chainrings get auto sorted to Small/Large (e.g 50/34 becomes 34/50 internally)


  The valid syntex for cassete models is:

  CS-MXXXX [Range] (MTB)
  
  CS-RXXXX [Range] (Road)
  
  CS-HGXXX [Range] (General purpose HG Cassetes)
  
  alternatively check cassettes.json for the entire list
  
  ### Advice for interpreting results
  
  This is personal preference (wich is why you can tune it)
  but generally you want to choose the crossover that:
  - has a gear step close to what comes before and after
  - isn't too big, neither too small
  - happens in the middle of the cassete
  - does not severely bias a certain ring 
  
This tool is meant to save you from creating spreadsheets to calculate the possible crossover, i hope it does so.

### more to come
botique makers cassettes will follow eventually
