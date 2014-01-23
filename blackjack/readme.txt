
here's what I have in mind:

computeOddsForHand_playerTurn(playerHand, dealerHand):
  stand odds -> computeOddsForHand_dealerTurn(playerHand, dealerHand)
  hit odds ->
    for each possible card
      add that card to your (original) hand
      if you busted, count -bet
      if not, computeOddsForHand_playerTurn(playerHand, dealerHand)
    odds = average of all those
  surrender odds -> always -bet/2
  double odds ->
    bet *= 2
    then same as hit odds, except you don't need to recurse
  split odds ->
    for each possible card
      add that card to the first hand
      computeOddsForHand_playerTurn(hand1, dealerHand)
    odds1 = average all of those
    for each possible card
      add that card to the second hand
      computeOddsForHand_playerTurn(hand2, dealerHand)
    odds2 = average of all of those
    totalodds = odds1 + odds2

  choose best of all possible odds

computeOddsForHand_dealerTurn(playerHand, dealerHand):
  if dealer has <17:
    for each possible card
      add that card to the dealer's (original) hand
      if he busted, count +bet
      if not, computeOddsForHand_dealerTurn(playerHand, dealerHand)
    odds = average of all those
  else dealer stands:
    odds = 'bet' if player better, 0 if equal, -bet if dealer better
