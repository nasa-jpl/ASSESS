import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
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
import org.xml.sax.SAXException;

/**
 * StandardsExtractor performs the extraction of the scope within the given 
 * document, add the scope to the Metadata object, and finally serializes the 
 * metadata to JSON.
 *
 */
public class StandardsExtractor {
	public static final String SCOPE = "scope";
	private static final String REGEX_SCOPE = "(?<index>\\d)\\.0?\\p{Blank}+(SCOPE)";

	public static void main(String[] args) {
		if (args.length < 2) {
			System.err.println("Usage: " + StandardsExtractionExample.class.getName() + " /path/to/input threshold");
			System.exit(1);
		}
		String pathname = args[0];
		double threshold = Double.parseDouble(args[1]);
		
		Path input = Paths.get(pathname);
		
		Metadata metadata = null;
		
		try {
			metadata = process(input, threshold);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		StringWriter writer = new StringWriter();
		JsonMetadata.setPrettyPrinting(true);
		
		try {
			JsonMetadata.toJson(metadata, writer);
		} catch (TikaException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		System.out.println(writer.toString());
	}
	
	private static Metadata process(Path input, double threshold) throws IOException, SAXException, TikaException {
		Parser parser = new AutoDetectParser();
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
		
		InputStream stream = new BufferedInputStream(Files.newInputStream(input));
		
		parser.parse(stream, handler, metadata, new ParseContext());
		
		String text = handler.toString();
		
		Pattern patternScope = Pattern.compile(REGEX_SCOPE);
		Matcher matcherScope = patternScope.matcher(text);
	
		// Gets the second occurrence of SCOPE
		for (int i = 0; i < 2; i++) {
			matcherScope.find();
		}
		
		int start = matcherScope.end();
		int index = Integer.parseInt(matcherScope.group("index")) + 1;
		
		//private static final String REGEX_SCOPE = "(?<index>\\d)\\.0?\\p{Blank}+(SCOPE)";
		Pattern patternNextHeader = Pattern.compile(index + "\\.0?\\p{Blank}+([A-Z]+(\\s[A-Z]+)*)");
		Matcher matcherNextHeader = patternNextHeader.matcher(text);
		
		int end = text.length();
		if (matcherNextHeader.find(start)) {
			end = matcherNextHeader.start();
		}
		
		//TODO Clean text by removing header, footer, and page number (try to find the patterns associated with header and footer)
		String scope = text.substring(start + 1, end);
		
		metadata.add(SCOPE, scope);
		
		return metadata;
	}
}