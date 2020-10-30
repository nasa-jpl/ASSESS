/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.tika.sax;

import java.util.Map;
import java.util.TreeMap;

/**
 * This class provides a collection of the most important technical standard organizations.
 * The collection of standard organizations has been obtained from <a href="https://en.wikipedia.org/wiki/List_of_technical_standard_organisations">Wikipedia</a>.
 * Currently, the list is composed of the most important international standard organizations, the regional standard organizations (i.e., Africa, Americas, Asia Pacific, Europe, and Middle East), and British and American standard organizations among the national-based ones.
 *
 */
public class StandardOrganizations {

	private static Map<String, String> organizations;
	static {
		organizations = new TreeMap<String, String>();
		//manually added organizations
		organizations.put("CFR", "Code of Federal Regulations");
		organizations.put("BIPM", "International Bureau of Weights and Measures");
		organizations.put("CGPM", "General Conference on Weights and Measures");
		organizations.put("CIPM", "International Committee for Weights and Measures");

		//International standard organizations
	    organizations.put("3GPP", "3rd Generation Partnership Project");
	    organizations.put("3GPP2", "3rd Generation Partnership Project 2");
	    organizations.put("ABYC", "The American Boat & Yacht Council");
	    organizations.put("Accellera", "Accellera Organization");
	    organizations.put("A4L", "Access for Learning Community");
	    organizations.put("AES", "Audio Engineering Society");
	    organizations.put("AIIM", "Association for Information and Image Management");
	    organizations.put("ASAM", "Association for Automation and Measuring Systems");
	    organizations.put("ASHRAE", "American Society of Heating, Refrigerating and Air-Conditioning Engineers");
	    organizations.put("ASME", "American Society of Mechanical Engineers");
	    organizations.put("ASTM", "American Society for Testing and Materials");
	    organizations.put("ATIS", "Alliance for Telecommunications Industry Solutions");
	    organizations.put("AUTOSAR", "Automotive technology");
	    //organizations.put("BIPM, CGPM, and CIPM", "Bureau International des Poids et Mesures and the related organizations established under the Metre Convention of 1875.");
	    organizations.put("CableLabs", "Cable Television Laboratories");
	    organizations.put("CCSDS", "Consultative Committee for Space Data Sciences");
	    organizations.put("CIE", "International Commission on Illumination");
	    organizations.put("CISPR", "International Special Committee on Radio Interference");
	    organizations.put("CFA", "Compact flash association");
	    organizations.put("DCMI", "Dublin Core Metadata Initiative");
	    organizations.put("DDEX", "Digital Data Exchange");
	    organizations.put("DMTF", "Distributed Management Task Force");
	    organizations.put("ECMA", "Ecma International");
	    organizations.put("EKOenergy", "EKOenergy");
	    organizations.put("FAI", "Fédération Aéronautique Internationale");
	    organizations.put("GS1", "Global supply chain standards");
	    organizations.put("HGI", "Home Gateway Initiative");
	    organizations.put("HFSB", "Hedge Fund Standards Board");
	    organizations.put("IATA", "International Air Transport Association");
	    organizations.put("IAU", "International Arabic Union");
	    organizations.put("ICAO", "International Civil Aviation Organization");
	    organizations.put("IEC", "International Electrotechnical Commission");
	    organizations.put("IEEE", "Institute of Electrical and Electronics Engineers");
	    organizations.put("IEEE-SA", "IEEE Standards Association");
	    organizations.put("IETF", "Internet Engineering Task Force");
	    organizations.put("IFOAM", "International Federation of Organic Agriculture Movements");
	    organizations.put("IFSWF", "International Forum of Sovereign Wealth Funds");
	    organizations.put("IMO", "International Maritime Organization");
	    organizations.put("IMS", "IMS Global Learning Consortium");
	    organizations.put("ISO", "International Organization for Standardization");
	    organizations.put("IPTC", "International Press Telecommunications Council");
	    organizations.put("ITU", "The International Telecommunication Union");
	    organizations.put("ITU-R", "ITU Radiocommunications Sector");
	    organizations.put("CCIR", "Comité Consultatif International pour la Radio");
	    organizations.put("ITU-T", "ITU Telecommunications Sector");
	    organizations.put("CCITT", "Comité Consultatif International Téléphonique et Télégraphique");
	    organizations.put("ITU-D", "ITU Telecom Development");
	    organizations.put("BDT", "Bureau de développement des télécommunications, renamed ITU-D");
	    organizations.put("IUPAC", "International Union of Pure and Applied Chemistry");
	    organizations.put("Liberty Alliance", "Liberty Alliance");
	    organizations.put("Media Grid", "Media Grid Standards Organization");
	    organizations.put("NACE International", "National Association of Corrosion Engineers");
	    organizations.put("OASIS", "Organization for the Advancement of Structured Information Standards");
	    organizations.put("OGC", "Open Geospatial Consortium");
	    organizations.put("OHICC", "Organization of Hotel Industry Classification & Certification");
	    organizations.put("OIF", "Optical Internetworking Forum");
	    organizations.put("OMA", "Open Mobile Alliance");
	    organizations.put("OMG", "Object Management Group");
	    organizations.put("OGF", "Open Grid Forum");
	    organizations.put("GGF", "Global Grid Forum");
	    organizations.put("EGA", "Enterprise Grid Alliance");
	    organizations.put("OTA", "OpenTravel Alliance");
	    organizations.put("OSGi", "OSGi Alliance");
	    organizations.put("PESC", "P20 Education Standards Council");
	    organizations.put("SAI", "Social Accountability International");
	    organizations.put("SDA", "Secure Digital Association");
	    organizations.put("SNIA", "Storage Networking Industry Association");
	    organizations.put("SMPTE", "Society of Motion Picture and Television Engineers");
	    organizations.put("SSDA", "Solid State Drive Alliance");
	    organizations.put("The Open Group", "The Open Group");
	    organizations.put("TIA", "Telecommunications Industry Association");
	    organizations.put("TM Forum", "Telemanagement Forum");
	    organizations.put("UIC", "International Union of Railways");
	    organizations.put("UL", "Underwriters Laboratories");
	    organizations.put("UPU", "Universal Postal Union");
	    organizations.put("WMO", "World Meteorological Organization");
	    organizations.put("W3C", "World Wide Web Consortium");
	    organizations.put("WSA", "Website Standards Association");
	    organizations.put("WHO", "World Health Organization");
	    organizations.put("XSF", "The XMPP Standards Foundation");
	    organizations.put("FAO", "Food and Agriculture Organization");
	    //Regional standards organizations
	    //Africa
	    organizations.put("ARSO", "African Regional Organization for Standarization");
	    organizations.put("SADCSTAN", "Southern African Development Community Cooperation in Standarization");
	    //Americas
	    organizations.put("COPANT", "Pan American Standards Commission");
	    organizations.put("AMN", "MERCOSUR Standardization Association");
	    organizations.put("CROSQ", "CARICOM Regional Organization for Standards and Quality");
	    organizations.put("AAQG", "America's Aerospace Quality Group");
	    //Asia Pacific
	    organizations.put("PASC", "Pacific Area Standards Congress");
	    organizations.put("ACCSQ", "ASEAN Consultative Committee for Standards and Quality");
	    //Europe
	    organizations.put("RoyalCert", "RoyalCert International Registrars");
	    organizations.put("CEN", "European Committee for Standardization");
	    organizations.put("CENELEC", "European Committee for Electrotechnical Standardization");
	    organizations.put("URS", "United Registrar of Systems, UK");
	    organizations.put("ETSI", "European Telecommunications Standards Institute");
	    organizations.put("EASC", "Euro-Asian Council for Standardization, Metrology and Certification");
	    organizations.put("IRMM", "Institute for Reference Materials and Measurements");
	    organizations.put("WELMEC", "European Cooperation in Legal Metrology");
	    organizations.put("EURAMET", "the European Association of National Metrology Institutes");
	    //Middle East
	    organizations.put("AIDMO", "Arab Industrial Development and Mining Organization");
	    organizations.put("IAU", "International Arabic Union");
	    //Nationally-based standards organizations
	    //United Kingdom
	    organizations.put("BSI", "British Standards Institution aka BSI Group");
	    organizations.put("DStan", "UK Defence Standardization");
	    //United States of America
	    organizations.put("ANSI", "American National Standards Institute");
	    organizations.put("ACI", "American Concrete Institute");
	    organizations.put("NIST", "National Institute of Standards and Technology");

	    //for and of the in on

	    //manually added organizations
	    organizations.put("Code\\sof\\sFederal\\sRegulations", "CFR");
		organizations.put("International\\sBureau\\sof\\sWeights\\sand\\sMeasures", "BIPM");
		organizations.put("General\\sConference\\son\\sWeights\\sand\\sMeasures", "CGPM");
		organizations.put("International\\sCommittee\\sfor\\sWeights\\sand\\sMeasures", "CIPM");

		//International standard organizations
	   	organizations.put("3rd\\sGeneration\\sPartnership\\sProject", "3GPP");
	    organizations.put("3rd\\sGeneration\\sPartnership\\sProject\\s2", "3GPP2");
	    organizations.put("The\\sAmerican\\sBoat\\s&\\sYacht\\sCouncil", "ABYC");
	    organizations.put("Accellera\\sOrganization", "Accellera");
	    organizations.put("Access\\sfor\\sLearning\\sCommunity", "A4L");
	    organizations.put("Audio\\sEngineering\\sSociety", "AES");
	    organizations.put("Association\\sfor\\sInformation\\sand\\sImage\\sManagement", "AIIM");
	    organizations.put("Association\\sfor\\sAutomation\\sand\\sMeasuring\\sSystems", "ASAM");
	    organizations.put("American\\sSociety\\sof\\sHeating,\\sRefrigerating\\sand\\sAir-Conditioning\\sEngineers", "ASHRAE");
	    organizations.put("American\\sSociety\\sof\\sMechanical\\sEngineers", "ASME");
	    organizations.put("American\\sSociety\\sfor\\sTesting\\sand\\sMaterials", "ASTM");
	    organizations.put("Alliance\\sfor\\sTelecommunications\\sIndustry\\sSolutions", "ATIS");
	    organizations.put("Automotive\\stechnology", "AUTOSAR");
	    //organizations.put("BIPM, CGPM, and CIPM", "Bureau International des Poids et Mesures and the related organizations established under the Metre Convention of 1875.");
	    organizations.put("Cable\\sTelevision\\sLaboratories", "CableLabs");
	    organizations.put("Consultative\\sCommittee\\sfor\\sSpace\\sData\\sSciences", "CCSDS");
	    organizations.put("International\\sCommission\\son\\sIllumination", "CIE");
	    organizations.put("International\\sSpecial\\sCommittee\\son\\sRadio\\sInterference", "CISPR");
	    organizations.put("Compact\\sflash\\sassociation", "CFA");
	    organizations.put("Dublin\\sCore\\sMetadata\\sInitiative", "DCMI");
	    organizations.put("Digital\\sData\\sExchange", "DDEX");
	    organizations.put("Distributed\\sManagement\\sTask\\sForce", "DMTF");
	    organizations.put("Ecma\\sInternational", "ECMA");
	    organizations.put("EKOenergy", "EKOenergy");
	    organizations.put("Fédération\\sAéronautique\\sInternationale", "FAI");
	    organizations.put("Global\\ssupply\\schain\\sstandards", "GS1");
	    organizations.put("Home\\sGateway\\sInitiative", "HGI");
	    organizations.put("Hedge\\sFund\\sStandards\\sBoard", "HFSB");
	    organizations.put("International\\sAir\\sTransport\\sAssociation", "IATA");
	    organizations.put("International\\sArabic\\sUnion", "IAU");
	    organizations.put("International\\sCivil\\sAviation\\sOrganization", "ICAO");
	    organizations.put("International\\sElectrotechnical\\sCommission", "IEC");
	    organizations.put("Institute\\sof\\sElectrical\\sand\\sElectronics\\sEngineers", "IEEE");
	    organizations.put("IEEE\\sStandards\\sAssociation", "IEEE-SA");
	    organizations.put("Internet\\sEngineering\\sTask\\sForce", "IETF");
	    organizations.put("International\\sFederation\\sof\\sOrganic\\sAgriculture\\sMovements", "IFOAM");
	    organizations.put("International\\sForum\\sof\\sSovereign\\sWealth\\sFunds", "IFSWF");
	    organizations.put("International\\sMaritime\\sOrganization", "IMO");
	    organizations.put("IMS\\sGlobal\\sLearning\\sConsortium", "IMS");
	    organizations.put("International\\sOrganization\\sfor\\sStandardization", "ISO");
	    organizations.put("International\\sPress\\sTelecommunications\\sCouncil", "IPTC");
	    organizations.put("The\\sInternational\\sTelecommunication\\sUnion", "ITU");
	    organizations.put("ITU\\sRadiocommunications\\sSector", "ITU-R");
	    organizations.put("Comité\\sConsultatif\\sInternational\\spour\\sla\\sRadio", "CCIR");
	    organizations.put("ITU\\sTelecommunications\\sSector", "ITU-T");
	    organizations.put("Comité\\sConsultatif\\sInternational\\sTéléphonique\\set\\sTélégraphique", "CCITT");
	    organizations.put("ITU\\sTelecom\\sDevelopment", "ITU-D");
	    organizations.put("Bureau\\sde\\sdéveloppement\\sdes\\stélécommunications", "BDT");
	    organizations.put("International\\sUnion\\sof\\sPure\\sand\\sApplied\\sChemistry", "IUPAC");
	    organizations.put("Liberty Alliance", "Liberty Alliance");
	    organizations.put("Media\\sGrid\\sStandards\\sOrganization", "Media Grid");
	    organizations.put("National\\sAssociation\\sof\\sCorrosion\\sEngineers", "NACE International");
	    organizations.put("Organization\\sfor\\sthe\\sAdvancement\\sof\\sStructured\\sInformation\\sStandards", "OASIS");
	    organizations.put("Open\\sGeospatial\\sConsortium", "OGC");
	    organizations.put("Organization\\sof\\sHotel\\sIndustry\\sClassification\\s&\\sCertification", "OHICC");
	    organizations.put("Optical\\sInternetworking\\sForum", "OIF");
	    organizations.put("Open\\sMobile\\sAlliance", "OMA");
	    organizations.put("Object\\sManagement\\sGroup", "OMG");
	    organizations.put("Open\\sGrid\\sForum", "OGF");
	    organizations.put("Global\\sGrid\\sForum", "GGF");
	    organizations.put("Enterprise\\sGrid\\sAlliance", "EGA");
	    organizations.put("OpenTravel\\sAlliance", "OTA");
	    organizations.put("OSGi\\sAlliance", "OSGi");
	    organizations.put("P20\\sEducation\\sStandards\\sCouncil", "PESC");
	    organizations.put("Social\\sAccountability\\sInternational", "SAI");
	    organizations.put("Secure\\sDigital\\sAssociation", "SDA");
	    organizations.put("Storage\\sNetworking\\sIndustry\\sAssociation", "SNIA");
	    organizations.put("Society\\sof\\sMotion\\sPicture\\sand\\sTelevision\\sEngineers", "SMPTE");
	    organizations.put("Solid\\sState\\sDrive\\sAlliance", "SSDA");
	    organizations.put("The\\sOpen\\sGroup", "The Open Group");
	    organizations.put("Telecommunications\\sIndustry\\sAssociation", "TIA");
	    organizations.put("Telemanagement\\sForum", "TM Forum");
	    organizations.put("International\\sUnion\\sof\\sRailways", "UIC");
	    organizations.put("Underwriters\\sLaboratories", "UL");
	    organizations.put("Universal\\sPostal\\sUnion", "UPU");
	    organizations.put("World\\sMeteorological\\sOrganization", "WMO");
	    organizations.put("World\\sWide\\sWeb\\sConsortium", "W3C");
	    organizations.put("Website\\sStandards\\sAssociation", "WSA");
	    organizations.put("World\\sHealth\\sOrganization", "WHO");
	    organizations.put("The\\sXMPP\\sStandards\\sFoundation", "XSF");
	    organizations.put("Food\\sand\\sAgriculture\\sOrganization", "FAO");
	    //Regional standards organizations
	    //Africa
	    organizations.put("African\\sRegional\\sOrganization\\sfor\\sStandarization", "ARSO");
	    organizations.put("Southern\\sAfrican\\sDevelopment\\sCommunity\\sCooperation\\sin\\sStandarization", "SADCSTAN");
	    //Americas
	    organizations.put("Pan\\sAmerican\\sStandards\\sCommission", "COPANT");
	    organizations.put("MERCOSUR\\sStandardization\\sAssociation", "AMN");
	    organizations.put("CROSQ", "CARICOM\\sRegional\\sOrganization\\sfor\\sStandards\\sand\\sQuality");
	    organizations.put("America's\\sAerospace\\sQuality\\sGroup", "AAQG");
	    //Asia Pacific
	    organizations.put("Pacific\\sArea\\sStandards\\sCongress", "PASC");
	    organizations.put("ASEAN\\sConsultative\\sCommittee\\sfor\\sStandards\\sand\\sQuality", "ACCSQ");
	    //Europe
	    organizations.put("RoyalCert\\sInternational\\sRegistrars", "RoyalCert");
	    organizations.put("European\\sCommittee\\sfor\\sStandardization", "CEN");
	    organizations.put("European\\sCommittee\\sfor\\sElectrotechnical\\sStandardization", "CENELEC");
	    organizations.put("United\\sRegistrar\\sof\\sSystems", "URS");
	    organizations.put("European\\sTelecommunications\\sStandards\\sInstitute", "ETSI");
	    organizations.put("Euro-Asian\\sCouncil\\sfor\\sStandardization,\\sMetrology\\sand\\sCertification", "EASC");
	    organizations.put("Institute\\sfor\\sReference\\sMaterials\\sand\\sMeasurements", "IRMM");
	    organizations.put("European\\sCooperation\\sin\\sLegal\\sMetrology", "WELMEC");
	    organizations.put("the\\sEuropean\\sAssociation\\sof\\sNational\\sMetrology\\sInstitutes", "EURAMET");
	    //Middle East
	    organizations.put("Arab\\sIndustrial\\sDevelopment\\sand\\sMining\\sOrganization", "AIDMO");
	    organizations.put("International\\sArabic\\sUnion", "IAU");
	    //Nationally-based standards organizations
	    //United Kingdom
	    organizations.put("British\\sStandards\\sInstitution", "BSI");
	    organizations.put("UK\\sDefence\\sStandardization", "DStan");
	    //United States of America
	    organizations.put("American\\sNational\\sStandards\\sInstitute", "ANSI");
	    organizations.put("American\\sConcrete\\sInstitute", "ACI");
	    organizations.put("National\\sInstitute\\sof\\sStandards\\sand\\sTechnology", "NIST");
	    
    }
	 		
	/**
	 * Returns the map containing the collection of the most important technical standard organizations.
	 * 
	 * @return the map containing the collection of the most important technical standard organizations.
	 */
	public static Map<String, String> getOrganizations() {
		return organizations;
	}
	
	/**
	 * Returns the regular expression containing the most important technical standard organizations.
	 * 
	 * @return the regular expression containing the most important technical standard organizations.
	 */
	public static String getOrganzationsRegex() {
		String regex = "(" + String.join("|", organizations.keySet()) + ")"; //1) regex improved, 2) take care of white space w/ second fxn
		return regex;
	}
}