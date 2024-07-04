USE [test]
GO
/****** Object:  Table [dbo].[areaCalculationSheet_Formulas]    Script Date: 20-06-2024 15:14:28 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[areaCalculationSheet_Formulas](
	[Formula] [nvarchar](max) NULL,
	[Column_Header] [nvarchar](255) NULL,
	[CellName] [nvarchar](255) NULL,
	[Involved_Columns] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
