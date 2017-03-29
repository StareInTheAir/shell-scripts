# Haskell knowledge

## mapMaybe
	Prelude Data.Maybe> Data.Maybe.mapMaybe (\i -> if i==1 then Nothing else Just i) [1,2,3]
	[2,3]

## sequence
sequence :: [Maybe a] -> Maybe [a]

	Prelude Data.Maybe> sequence [Just 1, Just 2, Nothing]
	Nothing
	Prelude Data.Maybe> sequence [Just 1, Just 2]
	Just [1,2]

## mapM
mapM f is equivalent to sequence . map f:

	Prelude Data.Maybe> sequence (map (\a -> if a==1 then Just (a+1) else Nothing) [1,2,3])
	Nothing
	Prelude Data.Maybe> sequence (map (\a -> if a==1 then Just (a+1) else Just a) [1,2,3])
	Just [2,2,3]
	Prelude Data.Maybe> mapM (\a -> if a==1 then Just (a+1) else Just a) [1,2,3]
	Just [2,2,3]
	Prelude Data.Maybe> mapM (\a -> if a==1 then Just (a+1) else Nothing) [1,2,3]
	Nothing
	
## stack ghci libraries
	stack ghci [--no-load]
	Prelude> :set -package hspec
	Prelude> import Test.Hspec

## ghci multiline input
	:set +m

## ghci language features
	:set -XOverloadedStrings