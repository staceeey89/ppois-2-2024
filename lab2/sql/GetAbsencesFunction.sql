ALTER FUNCTION GetAbsences(@reason Nvarchar(50), @studentId uniqueidentifier) RETURNS INTEGER

AS
BEGIN
  DECLARE @num INTEGER

  set @num= (select Count(*) as AbsencesCount from Students as St
				inner join Absences as Abs on (Abs.StudentId = St.Id)
				where Abs.ReasonId = (select Reasons.Id from AbsenceReasons as Reasons
				where Reasons.Name = @reason)
				and St.Id = @studentId
				Group by St.Id, ReasonId)

  RETURN @num
END

--select St.Id, dbo.GetAbsences('other', St.Id) as AbsenceCount from Students as St
