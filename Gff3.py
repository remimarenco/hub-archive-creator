#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Gff3( Datatype ):
    def __init__(self, input_Gff3_false_path, data_gff3):
        super( Gff3, self ).__init__()

        self.track = None

        self.input_Gff3_false_path = input_Gff3_false_path
        self.name_gff3 = data_gff3["name"]
        self.priority = data_gff3["order_index"]

        # TODO: See if we need these temporary files as part of the generated files
        unsorted_genePred_file = tempfile.NamedTemporaryFile(bufsize=0, suffix=".genePred")
        # unsortedBedFile = tempfile.NamedTemporaryFile(bufsize=0, suffix=".unsortedBed")
        sorted_genePred_file = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        # TODO: Refactor into another Class to manage the twoBitInfo and ChromSizes (same process as in Gtf.py)

        # gff3ToGenePred processing
        subtools.gff3ToGenePred(self.input_Gff3_false_path, unsorted_genePred_file.name)

        # Sort processing
        subtools.sort(unsorted_genePred_file.name, sorted_genePred_file.name)

        # genePredToBed processing
        #subtools.genePredToBed(genePredFile.name, unsortedBedFile.name)

        # TODO: Check if no errors

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( (self.name_gff3, ".bb" ) )

        auto_sql_option = "%s%s" % ('-as=', os.path.join(self.tool_directory, 'bigGenePred.as'))

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)

        with open(myBigBedFilePath, 'w') as bigBedFile:
            subtools.bedToBigBed(sorted_genePred_file.name,
                                 self.chromSizesFile.name,
                                 bigBedFile.name,
                                 autoSql=auto_sql_option,
                                 typeOption='-type=bed12+8')

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_gff3, track_type='bigGenePred', visibility='dense', priority=self.priority,
                         track_file=myBigBedFilePath)

        print("- Gff3 %s created" % self.name_gff3)
