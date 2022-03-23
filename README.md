# IBM Machine Translation

This is a finilized copy of my machine translation lab work for Natural Language Processing (CS065). I am putting it on my own github because my teammate and I worked really hard on this lab and developed it really well. We are proud of our work and we want to show it to the world. 

## About the Program

This program follows Charniak's book on Natural Language Processing, specifically on Machine Translation. Follow this [link] (https://drive.google.com/file/d/1yFd6TfnETLxG1eN-w-vCnsJwDkrXD0Ms/view) to find more information about the details and concepts of the IBM Model. 

### IBM Model I

The IBM Model uses a simple noisy channel model to compute the probability of a destination word (English) given a source word (French). The program is built so that it can take any parallel data for any language to output a trained model. Using this model we can translate any input language to the desired output language. 

### Very Dumb Decoder

To put our IBM model to test, we have also implemented a decoder that goes through an entire sentence or an entire document and translated it. This decode doesn't do anything fancy but just calls the IBM Translators special translate methods on each word in a document.

### Noisy Channel Decoder

This decoder is a bit more complex in that it takes into account the context of a word before it translates it. This will allow it to make a better often human readable translation. 

### F Score

Both the Very Dumb Decoder and the Noisy Channel Decoder aren't state of the art and don't do a pretty good job of because their inheret decoder is limited in its ability to translate well. Our F score can help us test how well our decoders are working. It takes in the expected output and the output either of the decoders made and creates a score from 0 to 1. 

# ibm-machine-translation
