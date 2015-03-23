DROP TABLE IF EXISTS "Transcript_Protein";
DROP TABLE IF EXISTS "Gene_Transcript";
DROP TABLE IF EXISTS "Gene";
DROP TABLE IF EXISTS "Protein";
DROP TABLE IF EXISTS "Transcript";
CREATE TABLE "Gene" ("ensembleID" TEXT PRIMARY KEY, "species" TEXT NOT NULL, "entrezID" TEXT);
CREATE TABLE "Transcript" ("transcriptID" TEXT PRIMARY KEY, "downstream" TEXT);
CREATE TABLE "Protein" ("proteinID" TEXT PRIMARY KEY);

CREATE TABLE "Gene_Transcript" (
    "ensembleID" TEXT REFERENCES "Gene" ("ensembleID") ON DELETE CASCADE ON UPDATE CASCADE,
    "transcriptID" TEXT REFERENCES "Transcript" ("transcriptID") ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (ensembleID,transcriptID));

CREATE TABLE "Transcript_Protein" (
    "transcriptID" TEXT REFERENCES "Transcript" ("transcriptID") ON DELETE CASCADE ON UPDATE CASCADE,
    "proteinID" TEXT REFERENCES "Protein" ("proteinID") ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY(transcriptID,proteinID));
