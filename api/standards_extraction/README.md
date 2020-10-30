# StandardsExtractingContentHandler

Apache Tika currently provides many _ContentHandler_ which help to de-obfuscate specific types of information from text. For instance, the `PhoneExtractingContentHandler` is used to extract phone numbers while parsing.

This improvement adds the **`StandardsExtractingContentHandler`** to Tika, a new ContentHandler that relies on regular expressions in order to identify and extract standard references from text. 
Basically, a standard reference is just a reference to a norm/convention/requirement (i.e., a standard) released by a standard organization. This work is maily focused on identifying and extracting the references to the standards already cited within a given document (e.g., SOW/PWS) so the references can be stored and provided to the user as additional metadata in case the `StandardExtractingContentHandler` is used.

In addition to the patch, the first version of the `StandardsExtractingContentHandler` along with an example class to easily execute the handler is available on [GitHub](https://github.com/giuseppetotaro/StandardsExtractingContentHandler). The following sections provide more in detail how the `StandardsExtractingHandler` has been developed.

All the details are reported on Jira ([TIKA-2449](https://issues.apache.org/jira/browse/TIKA-2449)).

## Getting Started

To build StandardsExtractingContentHandler, you can run the following bash script:

```
./build.sh
```

To extract standard references by using the StandardsExtractingContentHandler, you can run the following bash script: 

```
./run.sh /path/to/input threshold
```

For instance, by running `./run.sh ./example/SOW-TacCOM.pdf 0.75` you can get the standard references from the [SOW-TacCOM.pdf](https://foiarr.cbp.gov/streamingWord.asp?i=607) file using a threshold of 0.75 along with the scope and other metadata:

```
{
  "Author": "BAF107S",
  "Content-Type": "application/pdf",
  "Creation-Date": "2011-04-21T21:36:36Z",
  "Last-Modified": "2011-06-14T22:04:53Z",
  "Last-Save-Date": "2011-06-14T22:04:53Z",
  "X-Parsed-By": [
    "org.apache.tika.parser.DefaultParser",
    "org.apache.tika.parser.pdf.PDFParser"
  ],
  "access_permission:assemble_document": "false",
  "access_permission:can_modify": "false",
  "access_permission:can_print": "true",
  "access_permission:can_print_degraded": "false",
  "access_permission:extract_content": "false",
  "access_permission:extract_for_accessibility": "true",
  "access_permission:fill_in_form": "false",
  "access_permission:modify_annotations": "false",
  "created": "Thu Apr 21 14:36:36 PDT 2011",
  "creator": "BAF107S",
  "date": "2011-06-14T22:04:53Z",
  "dc:creator": "BAF107S",
  "dc:format": "application/pdf; version\u003d1.7",
  "dc:title": "Microsoft Word - SOW HSBP1010C00056.doc",
  "dcterms:created": "2011-04-21T21:36:36Z",
  "dcterms:modified": "2011-06-14T22:04:53Z",
  "meta:author": "BAF107S",
  "meta:creation-date": "2011-04-21T21:36:36Z",
  "meta:save-date": "2011-06-14T22:04:53Z",
  "modified": "2011-06-14T22:04:53Z",
  "pdf:PDFVersion": "1.7",
  "pdf:docinfo:created": "2011-04-21T21:36:36Z",
  "pdf:docinfo:creator": "BAF107S",
  "pdf:docinfo:creator_tool": "PScript5.dll Version 5.2.2",
  "pdf:docinfo:modified": "2011-06-14T22:04:53Z",
  "pdf:docinfo:producer": "Acrobat Distiller 9.3.3 (Windows)",
  "pdf:docinfo:title": "Microsoft Word - SOW HSBP1010C00056.doc",
  "pdf:encrypted": "true",
  "producer": "Acrobat Distiller 9.3.3 (Windows)",
  "scope": "\n \nThe purpose of this SOW is to describe the products and services that the Contractor \nwill provide to the CBP, Office of Information and Technology’s (OIT), Enterprise \n\n\n\nCBP TACCOM LMR Deployment Equipment and Services - Houlton Ref. No.____________  \nSource Selection Sensitive Information – See FAR 2.101 and 3.104 \n\n \n\n \nUpdated 02/25/10 2 \n\nSource Selection Sensitive Information – See FAR 2.101 and 3.104 \n \n\nNetworks and Technology Support (ENTS), Wireless Technology Programs (WTP) \nTACCOM Project in support of the TACCOM system modernization in the Houlton, \nMaine Focus Area 1.   \n \nThe Contractor shall provide LMR Equipment, Development, Deployment and Support \nas needed in support of CBP’s LMR network and systems. LMR Equipment, \nDevelopment, Deployment and Support includes, but is not limited to: assistance in \nengineering design and analysis, site development, equipment configuration, system \ninstallation, system testing, training, warehousing, transportation, field operations \nsupport, and equipment and material supply as called for within this SOW. \n \nThe equipment and services requested under this SOW will be applied in coordination \nwith the Government Contracting Officer’s Technical Representative (COTR), and/or the \nCOTR-designated Task Monitor(s). \n \n \n",
  "standard_references": [
    "ANSI/TIA 222-G",
    "TIA/ANSI 222-G-1",
    "FIPS 140-2",
    "FIPS 197"
  ],
  "title": "Microsoft Word - SOW HSBP1010C00056.doc",
  "xmp:CreatorTool": "PScript5.dll Version 5.2.2",
  "xmpMM:DocumentID": "uuid:13a50f6e-93d9-42f0-b939-eb9aa2c15426",
  "xmpTPg:NPages": "46"
}
```

## Background

From a technical perspective, a standard reference is a string that is usually composed of two parts: 
1. the name of the standard organization; 
2.  the alphanumeric identifier of the standard within the organization. 
Specifically, the first part can include the acronym or the full name of the standard organization or even both, and the second part can include an alphanumeric string, possibly containing one or more separation symbols (e.g., "-", "_", ".") depending on the format adopted by the organization, representing the identifier of the standard within the organization.

Furthermore, the standard references are usually reported within the "Applicable Documents" or "References" section of a SOW, and they can be cited also within sections that include in the header the word "standard", "requirement", "guideline", or "compliance".

Consequently, the citation of standard references within a SOW/PWS document can be summarized by the following rules:
* **RULE 1**: standard references are usually reported within the section named "Applicable Documents" or "References".
* **RULE 2**: standard references can be cited also within sections including the word "compliance" or another semantically-equivalent word in their name.
* **RULE 3**: standard references is composed of two parts:
  * Name of the standard organization (acronym, full name, or both).
  * Alphanumeric identifier of the standard within the organization.
* **RULE 4**: The name of the standard organization includes the acronym or the full name or both. The name must belong to the set of standard organizations `S = O U V`, where `O` represents the set of open standard organizations (e.g., ANSI) and `V` represents the set of vendor-specific standard organizations (e.g., Motorola).
* **RULE 5**: A separation symbol (e.g., "-", "_", "." or whitespace) can be used between the name of the standard organization and the alphanumeric identifier.
* **RULE 6**: The alphanumeric identifier of the standard is composed of alphabetic and numeric characters, possibly split in two or more parts by a separation symbol (e.g., "-", "_", ".").

On the basis of the above rules, here are some examples of formats used for reporting standard references within a SOW/PWS:
* `<ORGANIZATION_ACRONYM><SEPARATION_SYMBOL><ALPHANUMERIC_IDENTIFIER>`
* `<ORGANIZATION_ACRONYM><SEPARATION_SYMBOL>(<ORGANIZATION_FULL_NAME>)<SEPARATION_SYMBOL><ALPHANUMERIC_IDENTIFIER>`
* `<ORGANIZATION_FULL_NAME><SEPARATION_SYMBOL>(<ORGANIZATION_FULL_NAME>)<SEPARATION_SYMBOL><ALPHANUMERIC_IDENTIFIER>`

Moreover, some standards are sometimes released by two standard organizations. In this case, the standard reference can be reported as follows:
* `<MAIN_ORGANIZATION_ACRONYM>/<SECOND_ORGANIZATION_ACRONYM><SEPARATION_SYMBOL><ALPHANUMERIC_IDENTIFIER>`

## Regular Expressions

The `StandardsExtractingContentHandler` uses a helper class named `StandardsText` that relies on Java regular expressions and provides some methods to identify headers and standard references, and determine the score of the references found within the given text.

Here are the main regular expressions used within the `StandardsText` class:
* **REGEX_HEADER**: regular expression to match only uppercase headers.
  ```
  (\d+\.(\d+\.?)*)\p{Blank}+([A-Z]+(\s[A-Z]+)*){5,}
  ```
* **REGEX_APPLICABLE_DOCUMENTS**: regular expression to match the the header of "APPLICABLE DOCUMENTS" and equivalent sections.
  ```
  (?i:.*APPLICABLE\sDOCUMENTS|REFERENCE|STANDARD|REQUIREMENT|GUIDELINE|COMPLIANCE.*)
  ```
* **REGEX_FALLBACK**: regular expression to match a string that is supposed to be a standard reference.
  ```
  \(?(?<mainOrganization>[A-Z]\w+)\)?((\s?(?<separator>\/)\s?)(\w+\s)*\(?(?<secondOrganization>[A-Z]\w+)\)?)?(\s(Publication|Standard))?(-|\s)?(?<identifier>([0-9]{3,}|([A-Z]+(-|_|\.)?[0-9]{2,}))((-|_|\.)?[A-Z0-9]+)*)
  ```
* **REGEX_STANDARD**: regular expression to match the standard organization within a string potentially representing a standard reference.
  This regular expression is obtained by using a helper class named `StandardOrganizations` that provides a list of the most important standard organizations reported on [Wikipedia](https://en.wikipedia.org/wiki/List_of_technical_standard_organisations). Basically, the list is composed of International standard organizations, Regional standard organizations, and American and British among Nationally-based standard organizations. Other lists of standard organizations are reported on [OpenStandards](http://www.openstandards.net/viewOSnet2C.jsp?showModuleName=Organizations) and [IBR Standards Portal](https://ibr.ansi.org/Standards/).

## How To Use The Standards Extraction Capability

The standard references identification performed by using the `StandardsExtractingContentHandler` is based on the following steps (see also the [flow chart](https://issues.apache.org/jira/secure/attachment/12885939/flowchart_standards_extraction_v02.png)):
1. searches for headers;
2. searches for patterns that are supposed to be standard references (basically, every string mostly composed of uppercase letters followed by an alphanumeric characters);
3. each potential standard reference starts with score equal to 0.25;
4. increases by 0.25 the score of references which include the name of a known standard organization;
5. increases by 0.25 the score of references which include the word "Publication" or "Standard";
6. increases by 0.25 the score of references which have been found within "Applicable Documents" and equivalent sections;
7. returns the standard references along with scores;
8. adds the standard references as additional metadata.

The unit test is implemented within the **`StandardsExtractingContentHandlerTest`** class and extracts the standard references from a SOW downloaded from the [FOIA Library](https://foiarr.cbp.gov/streamingWord.asp?i=607). This SOW is also provide on [Jira](https://issues.apache.org/jira/secure/attachment/12884323/SOW-TacCOM.pdf).

The **`StandardsExtractionExample`** is a class to demonstrate how to use the `StandardsExtractingContentHandler` to get a list of the standard references from every file in a directory.
