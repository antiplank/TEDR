# TEDR
A dice rolling Discord bot for The Expanse Roleplaying Game. Rolls any number of dice or facets with an optional modifier and description. Doubles will be bolded and a drama die will be displayed on a roll of a 3d6. The bot will display an embed in the channel it was invoked, with a heading showing the user that invoked it. Triggering message will be deleted after the roll.

Usage: `!e xdy <mod> <description>`
  
Examples:
  
`!e 3d6 5`
  
`!e 4d12 -5`
  
`!e 3d6 1 Initiative(Bob)` <- Important to not have spaces for description
  
`!e 4d6 2 Damage(Eddie)` <- Important to not have spaces for description

## GM Rolls:
If you want the results of the roll to be sent to you in a DM

Usage: `!edm xdy <mod> <description>'

`!edm 3d6 5`
  
`!edm 4d12 -5`
  
`!edm 3d6 1 Initiative(Bob)` <- Important to not have spaces for description
  
`!edm 4d6 2 Damage(Eddie)` <- Important to not have spaces for description


## Churn Counter:
Keeps track of the churn with a graphical display.

Usage: `!churn <num>`

`!churn`          <- Displays the current churn
`!churn <num>` <- Adds or subtracts (when passed "-x") from the churn
`!churn reset`    <- Resets the churn to zero


This is a labor of love for myself and my friends, please don't think that I take this any more seriously than it deserves :)
