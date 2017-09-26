import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.metadata.serialization.JsonMetadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.parser.ocr.TesseractOCRConfig;
import org.apache.tika.parser.pdf.PDFParserConfig;
import org.apache.tika.sax.BodyContentHandler;
import org.apache.tika.sax.StandardsExtractingContentHandler;
import org.apache.tika.sax.StandardsExtractionExample;

/**
 * StandardsExtractor performs the extraction of the scope within the given 
 * document, add the scope to the Metadata object, and finally serializes the 
 * metadata to JSON.
 *
 */
public class StandardsExtractor {
	public static final String SCOPE = "scope";
	private static final String REGEX_SCOPE = "(?<index>(\\d\\.?)+)\\p{Blank}+(SCOPE|Scope)";

	public static void main(String[] args) {
		if (args.length < 2) {
			System.err.println("Usage: " + StandardsExtractionExample.class.getName() + " /path/to/input threshold");
			System.exit(1);
		}
		String pathname = args[0];
		double threshold = Double.parseDouble(args[1]);
		
		Path input = Paths.get(pathname);
		
		if (!Files.exists(input)) {
			System.err.println("Error: " + input + " does not exist!");
			System.exit(1);
		}
		
		Metadata metadata = null;
		
		try {
			metadata = process(input, threshold);
		} catch (Exception e) {
			metadata = new Metadata();
		}
		
		StringWriter writer = new StringWriter();
		JsonMetadata.setPrettyPrinting(true);
		
		try {
			JsonMetadata.toJson(metadata, writer);
		} catch (TikaException e) {
			writer.write("{}");
		}
		
		System.out.println(writer.toString());
	}
	
	private static Metadata process(Path input, double threshold) throws Exception {
		Parser parser = new AutoDetectParser();
//		ForkParser forkParser = new ForkParser(StandardsExtractor.class.getClassLoader(), parser);
		Metadata metadata = new Metadata();
		StandardsExtractingContentHandler handler = new StandardsExtractingContentHandler(new BodyContentHandler(-1), metadata);
		handler.setThreshold(threshold);
		
		TesseractOCRConfig ocrConfig = new TesseractOCRConfig();
	    PDFParserConfig pdfConfig = new PDFParserConfig();
	    pdfConfig.setExtractInlineImages(true);

	    ParseContext parseContext = new ParseContext();
	    parseContext.set(TesseractOCRConfig.class, ocrConfig);
	    parseContext.set(PDFParserConfig.class, pdfConfig);
	    parseContext.set(Parser.class, parser);

		try (InputStream stream = new BufferedInputStream(Files.newInputStream(input))) {
			parser.parse(stream, handler, metadata, parseContext);
		} 
//		try {
//			//TODO ForkParser gives back text in a different format wrt AutoDetectParser!
//			forkParser.parse(stream, handler, metadata, parseContext);
//		} finally {
//			forkParser.close();
//		}
		
		String text = handler.toString();
		
		Pattern patternScope = Pattern.compile(REGEX_SCOPE);
		Matcher matcherScope = patternScope.matcher(text);
		
		Matcher matchResult = null;
		boolean match = false;
		String scope = "";
		
//		// Gets the second occurrence of SCOPE
//		for (int i = 0; i < 2; i++) {
//			match = matcherScope.find();
		
//		}
		// Gets the last occurrence of scope
		for (int i = 0; i < 2 && (match = matcherScope.find()); i++) {
			matchResult = (Matcher)matcherScope.toMatchResult();
		}
		
		if (matchResult != null && !matchResult.group().isEmpty()) {
			int start = matchResult.end();
			String index = matchResult.group("index");
						
			int end = text.length() - 1;
			match = false;
			String endsWithDot = (index.substring(index.length()-1).equals(".")) ? "." : "";
			String[] parts = index.split("\\.");
			
			do {
				if (parts.length > 0) {
//					int subindex = Integer.parseInt(parts[parts.length-1]) + 1;
					int partsLength = parts.length;
					int subindex = Integer.parseInt(parts[--partsLength]);
					while (subindex++ == 0 && partsLength > 0) {
						subindex = Integer.parseInt(parts[--partsLength]);
					}
					parts[partsLength] = Integer.toString(subindex);
					index = String.join(".", parts) + endsWithDot;
				}
				
				Pattern patternNextHeader = Pattern.compile(index + "\\p{Blank}+([A-Z]([A-Za-z]+\\s?)*)");
				Matcher matcherNextHeader = patternNextHeader.matcher(text);
				
				if (match = matcherNextHeader.find(start)) {
					end = matcherNextHeader.start();
				}
				
				if (parts.length > 0) {
					parts = Arrays.copyOfRange(parts, 0, parts.length-1);
				}
			} while (!match && parts.length > 0);
			
			//TODO Clean text by removing header, footer, and page number (try to find the patterns associated with header and footer)
			scope = text.substring(start + 1, end);
		}
		
		metadata.add(SCOPE, scope);
		
		return metadata;
	}
}