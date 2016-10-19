__all__ = ["CleanMdashesExtension", "StripWhitespaceExtension"]

from CleanMdashesExtension import CleanMdashesExtension
from StripWhitespaceExtension import StripWhitespaceExtension

def cleanup(text):
	try:
		text = CleanMdashesExtension().cleanup(text)
	except:
		print("Unexpected error:", sys.exc_info()[0])

	try:
		text = StripWhitespaceExtension().cleanup(text)
	except:
		print("Unexpected error:", sys.exc_info()[0])

	return text