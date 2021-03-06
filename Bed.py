#!/usr/bin/python

import os
import tempfile

# Internal dependencies
from Datatype import Datatype
from Track import Track
from TrackDb import TrackDb
from util import subtools


class Bed( Datatype ):
    def __init__( self, inputBedGeneric, data_bed_generic):
        super(Bed, self).__init__()

        self.track = None

        self.inputBedGeneric = inputBedGeneric

        self.sortedBedFile = tempfile.NamedTemporaryFile(suffix=".sortedBed")

        self.data_bed_generic = data_bed_generic
        self.name_bed_generic = self.data_bed_generic["name"]
        self.priority = self.data_bed_generic["order_index"]
        self.track_color = self.data_bed_generic["track_color"]
        # TODO: Think about how to avoid repetition of the group_name everywhere
        self.group_name = self.data_bed_generic["group_name"]


        # Sort processing
        subtools.sort(self.inputBedGeneric, self.sortedBedFile.name)

        # bedToBigBed processing
        # TODO: Change the name of the bb, to tool + genome + possible adding if multiple +  .bb
        trackName = "".join( ( self.name_bed_generic, ".bb") )

        myBigBedFilePath = os.path.join(self.myTrackFolderPath, trackName)
        with open(myBigBedFilePath, 'w') as self.bigBedFile:
            subtools.bedToBigBed(self.sortedBedFile.name,
                                 self.chromSizesFile.name,
                                 self.bigBedFile.name)

        # Create the Track Object
        self.createTrack(file_path=trackName,
                         track_name=trackName,
                         long_label=self.name_bed_generic, track_type='bigBed', visibility='dense',
                         priority=self.priority,
                         track_file=myBigBedFilePath,
                         track_color=self.track_color,
                         group_name=self.group_name)

        # dataURL = "tracks/%s" % trackName
        #
        # trackDb = TrackDb(
        #     trackName=trackName,
        #     longLabel=self.name_bed_generic,
        #     shortLabel=self.getShortName(self.name_bed_generic),
        #     trackDataURL=dataURL,
        #     trackType='bigBed',
        #     visibility='dense',
        #     thickDrawItem='on',
        #     priority=self.priority,
        # )
        #
        # # Return the BigBed track
        # self.track = Track(
        #     trackFile=myBigBedFilePath,
        #     trackDb=trackDb,
        # )

        print("- Bed %s created" % self.name_bed_generic)
        #print("- %s created in %s" % (trackName, myBigBedFilePath))
