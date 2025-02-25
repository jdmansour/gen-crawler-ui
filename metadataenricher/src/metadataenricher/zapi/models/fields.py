from enum import Enum


class Fields(str, Enum):
    COLLECTIONS_PROPERTIES_CCLOMLOCATION = "collections.properties.cclom:location"
    COLLECTIONS_PROPERTIES_CMTITLE = "collections.properties.cm:title"
    COLLECTIONS_PROPERTIES_SYSNODE_UUID = "collections.properties.sys:node-uuid"
    NODEREF_ID = "nodeRef.id"
    PROPERTIES_CCLOMCLASSIFICATION_KEYWORD = "properties.cclom:classification_keyword"
    PROPERTIES_CCLOMDURATION = "properties.cclom:duration"
    PROPERTIES_CCLOMGENERAL_DESCRIPTION = "properties.cclom:general_description"
    PROPERTIES_CCLOMGENERAL_KEYWORD = "properties.cclom:general_keyword"
    PROPERTIES_CCLOMGENERAL_LANGUAGE = "properties.cclom:general_language"
    PROPERTIES_CCLOMTITLE = "properties.cclom:title"
    PROPERTIES_CCMCOMPETENCE = "properties.ccm:competence"
    PROPERTIES_CCMCURRICULUM = "properties.ccm:curriculum"
    PROPERTIES_CCMEDUCATIONALCONTEXT = "properties.ccm:educationalcontext"
    PROPERTIES_CCMEDUCATIONALINTENDEDENDUSERROLE = "properties.ccm:educationalintendedenduserrole"
    PROPERTIES_CCMEDUCATIONALTYPICALAGERANGE = "properties.ccm:educationaltypicalagerange"
    PROPERTIES_CCMFSKRATING = "properties.ccm:fskRating"
    PROPERTIES_CCMOEH_AI_TEST_DATA = "properties.ccm:oeh_ai_test_data"
    PROPERTIES_CCMOEH_COURSE_COURSEMODE = "properties.ccm:oeh_course_coursemode"
    PROPERTIES_CCMOEH_LRT = "properties.ccm:oeh_lrt"
    PROPERTIES_CCMOEH_TAXONID_UNIVERSITY = "properties.ccm:oeh_taxonid_university"
    PROPERTIES_CCMTAXONID = "properties.ccm:taxonid"
    PROPERTIES_CCMWWWURL = "properties.ccm:wwwurl"

    def __str__(self) -> str:
        return str(self.value)
