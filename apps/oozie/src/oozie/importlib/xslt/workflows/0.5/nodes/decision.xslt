<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:workflow="uri:oozie:workflow:0.5" exclude-result-prefixes="workflow">

<xsl:template match="workflow:decision" xmlns:workflow="uri:oozie:workflow:0.5">

  <object model="oozie.decision" pk="0">
  </object>

</xsl:template>

<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
</xsl:stylesheet>