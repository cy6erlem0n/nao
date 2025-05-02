<?xml version="1.0" encoding="UTF-8" ?>
<Package name="NaoRockPaperScissors" format_version="5">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="behavior_1" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs>
        <Dialog name="Greeting" src="Greeting/Greeting.dlg" />
        <Dialog name="GameEntry" src="GameEntry/GameEntry.dlg" />
        <Dialog name="PlayAgain" src="PlayAgain/PlayAgain.dlg" />
    </Dialogs>
    <Resources>
        <File name="_metadata" src="_metadata" />
        <File name="swiftswords_ext" src="behavior_1/swiftswords_ext.mp3" />
    </Resources>
    <Topics>
        <Topic name="Greeting_enu" src="Greeting/Greeting_enu.top" topicName="Greeting" language="en_US" nuance="enu" />
        <Topic name="GameEntry_enu" src="GameEntry/GameEntry_enu.top" topicName="GameEntry" language="en_US" nuance="enu" />
        <Topic name="PlayAgain_enu" src="PlayAgain/PlayAgain_enu.top" topicName="PlayAgain" language="en_US" nuance="enu" />
        <Topic name="Greeting_ged" src="Greeting/Greeting_ged.top" topicName="Greeting" language="de_DE" nuance="ged" />
        <Topic name="PlayAgain_ged" src="PlayAgain/PlayAgain_ged.top" topicName="PlayAgain" language="de_DE" nuance="ged" />
    </Topics>
    <IgnoredPaths />
    <Translations auto-fill="en_US">
        <Translation name="translation_de_DE" src="translations/translation_de_DE.ts" language="de_DE" />
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
    </Translations>
</Package>
