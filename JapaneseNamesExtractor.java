package myextractor;

import org.atilika.kuromoji.Token;
import org.atilika.kuromoji.Tokenizer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class JapaneseNamesExtractor {
    
    private final Tokenizer tokenizer = Tokenizer.builder().build();
    
    public List<String> extractNames(String sentence) {
        final List<Token> tokens = tokenizer.tokenize(sentence);
        final List<String> names = new ArrayList<>();
        int pos = 0;
        int lastFoundPos = -2;
        StringBuilder currentName = new StringBuilder();
        for(Token token: tokens) {
            if(isName(token)) {
                if(lastFoundPos == pos-1) {
                    currentName.append(token.getSurfaceForm());
                    names.add(currentName.toString());
                    currentName.setLength(0);
                }
                else {
                    if(currentName.length() > 0) {
                        names.add(currentName.toString());
                    }
                    currentName.setLength(0);
                    currentName.append(token.getSurfaceForm());
                }
                lastFoundPos = pos;
            }
            pos++;
        }
        if(currentName.length() > 0) {
            names.add(currentName.toString());
        }
        return names;
    }
    
    private boolean isName(Token token) {
        return  Arrays.stream(token.getAllFeaturesArray())
                .collect(Collectors.toSet())
                .contains("人名");
    } 

    public static void main(String[] args) throws IOException {
        if(args.length!=1) {
            throw new RuntimeException("Must have exactly one argument!");
        }
        System.out.println(new JapaneseNamesExtractor().extractNames(args[0])
                .stream().collect(Collectors.joining(",")));
    }
}