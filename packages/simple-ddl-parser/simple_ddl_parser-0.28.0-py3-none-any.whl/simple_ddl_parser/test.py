from distutils.log import debug
from simple_ddl_parser import DDLParser
import pprint

results = DDLParser(
"""/****** Object:  Table [dbo].[TO_Requests]    Script Date: 9/29/2021 9:55:26 PM ******/
        SET ANSI_NULLS ON
        GO
        SET QUOTED_IDENTIFIER ON
        GO
        CREATE TABLE [dbo].[TO_Requests](
            [Request_ID] [int] IDENTITY(1,1) NOT NULL,
            [user_id] [int] NULL,
            [date_from] [smalldatetime] NULL,)
""").run(group_by_type=True)

pprint.pprint(results) 
