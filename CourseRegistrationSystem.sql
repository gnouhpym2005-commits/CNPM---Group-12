CREATE DATABASE CourseRegistrationSystem;
GO

USE CourseRegistrationSystem;
GO

CREATE TABLE Users (
    userID VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    createdAt DATETIME DEFAULT GETDATE()
);

CREATE TABLE Student (
    studentID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20),
    fullName VARCHAR(100) NOT NULL,
    dateOfBirth DATE,
    email VARCHAR(100),
    password VARCHAR(100),
    major VARCHAR(100),
    earnedCredits INT DEFAULT 0,
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE()
    FOREIGN KEY(userID) REFERENCES Users(userID)
);

CREATE TABLE Lecturer (
    lecturerID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20),
    fullName VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    password VARCHAR(100),
    department VARCHAR(100),
    title VARCHAR(50),
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE()
    FOREIGN KEY(userID) REFERENCES Users(userID)
);

CREATE TABLE Admin (
    adminID VARCHAR(20) PRIMARY KEY,
    userID VARCHAR(20),
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    fullName VARCHAR(100),
    email VARCHAR(100),
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(userID) REFERENCES Users(userID)
);

CREATE TABLE Subject (
    subjectID VARCHAR(20) PRIMARY KEY,
    subjectName VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    tuition DECIMAL(10,2),
    department VARCHAR(100),
    description VARCHAR(200),
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE()
);

CREATE TABLE Subject_Prerequisite (
    subjectID VARCHAR(20),
    prerequisiteID VARCHAR(20),
    PRIMARY KEY(subjectID, prerequisiteID),
    FOREIGN KEY(subjectID) REFERENCES Subject(subjectID),
    FOREIGN KEY(prerequisiteID) REFERENCES Subject(subjectID)
);

CREATE TABLE RegistrationPeriod (
    periodID VARCHAR(20) PRIMARY KEY,
    semesterName VARCHAR(100),
    startDate DATE,
    endDate DATE,
    regOpenDate DATETIME,
    regCloseDate DATETIME,
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE()
);

CREATE TABLE CourseClass (
    classID VARCHAR(20) PRIMARY KEY,
    subjectID VARCHAR(20) NOT NULL,
    lecturerID VARCHAR(20) NOT NULL,
    periodID VARCHAR(20) NOT NULL,
    room VARCHAR(50),
    dayOfWeek VARCHAR(10),
    startTime TIME,
    endTime TIME,
    maxCapacity INT,
    currentEnrolled INT DEFAULT 0,
    status VARCHAR(20),
    FOREIGN KEY(subjectID) REFERENCES Subject(subjectID),
    FOREIGN KEY(lecturerID) REFERENCES Lecturer(lecturerID),
    FOREIGN KEY(periodID) REFERENCES RegistrationPeriod(periodID)
);

CREATE TABLE Registration (
    regID VARCHAR(20) PRIMARY KEY,
    studentID VARCHAR(20) NOT NULL,
    classID VARCHAR(20) NOT NULL,
    periodID VARCHAR(20) NOT NULL,
    regDate DATETIME DEFAULT GETDATE(),
    status VARCHAR(20),
    createdAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(studentID) REFERENCES Student(studentID),
    FOREIGN KEY(classID) REFERENCES CourseClass(classID),
    FOREIGN KEY(periodID) REFERENCES RegistrationPeriod(periodID),
    UNIQUE(studentID, classID, periodID)
);

CREATE TABLE Grade (
    gradeID VARCHAR(20) PRIMARY KEY,
    regID VARCHAR(20) UNIQUE NOT NULL,
    midterm DECIMAL(5,2) check (midterm >= 0 and midterm <= 10),
    finalExam DECIMAL(5,2) check (finalExam >= 0 and finalExam <= 10),
    totalScore DECIMAL(5,2) check (totalScore >= 0 and totalScore <= 10),
    letterGrade VARCHAR(5),
    createdAt DATETIME DEFAULT GETDATE(),
    FOREIGN KEY(regID) REFERENCES Registration(regID)
);

INSERT INTO Student(studentID, fullName, dateOfBirth, email, password, major, earnedCredits, status) VALUES
('SV001','Nguyen Van An','2004-05-12','an@gmail.com','123456','Information Technology',45,'Active'),
('SV002','Tran Thi Binh','2004-09-20','binh@gmail.com','123456','Computer Science',60,'Active'),
('SV003','Le Minh Chau','2005-01-15','chau@gmail.com','123456','Software Engineering',20,'Active'),
('SV004','Pham Quoc Dat','2004-11-10','dat@gmail.com','123456','Information Systems',80,'Locked');

INSERT INTO Lecturer (lecturerID, fullName, email, password, department, title, status) VALUES
('GV001','Dr. Nguyen Van A','nva@university.edu','123456','Information Technology','Professor','Active'),
('GV002','Tran Thi B','ttb@university.edu','123456','Computer Science','Associate Professor','Active'),
('GV003','Le Van C','lvc@university.edu','123456','Software Engineering','Lecturer','Active');

INSERT INTO Admin (adminID, username, password, fullName, email, status) VALUES
('AD001','admin','admin123','System Administrator','admin@university.edu','Active');

INSERT INTO Subject (subjectID, subjectName, credits, tuition, department, description, status) VALUES
('SUB001','Programming Fundamentals',3,4500000,'IT','Basic programming','Active'),
('SUB002','Object-Oriented Programming',3,4500000,'IT','OOP with Python','Active'),
('SUB003','Database Systems',3,4500000,'IT','SQL Server Database','Active'),
('SUB004','Data Structures and Algorithms',4,6000000,'IT','DSA','Active'),
('SUB005','Computer Networks',3,4500000,'IT','Networking Fundamentals','Active');

INSERT INTO Subject_Prerequisite (subjectID, prerequisiteID) VALUES
('SUB002','SUB001'),
('SUB004','SUB002'),
('SUB003','SUB001');

INSERT INTO RegistrationPeriod (periodID, semesterName, startDate, endDate, regOpenDate, regCloseDate, status) VALUES
('P001',
'Semester 1 - 2026',
'2026-09-01',
'2026-12-31',
'2026-08-01 08:00',
'2026-08-15 17:00',
'Open');

INSERT INTO CourseClass
(classID, subjectID, lecturerID, periodID,
room, dayOfWeek, startTime, endTime,
maxCapacity, currentEnrolled, status)
VALUES

('CLS001','SUB001','GV001','P001',
'A101','Monday','07:30','09:30',
50,2,'Open'),

('CLS002','SUB002','GV002','P001',
'B201','Tuesday','09:30','11:30',
40,1,'Open'),

('CLS003','SUB003','GV003','P001',
'C301','Wednesday','13:00','15:00',
35,1,'Open'),

('CLS004','SUB004','GV001','P001',
'A202','Thursday','07:30','10:30',
30,0,'Open');

INSERT INTO Registration (regID, studentID, classID, periodID, status) VALUES
('REG001','SV001','CLS001','P001','Approved'),
('REG002','SV001','CLS003','P001','Approved'),
('REG003','SV002','CLS001','P001','Approved'),
('REG004','SV003','CLS002','P001','Pending');

INSERT INTO Grade (gradeID, regID, midterm, finalExam, totalScore, letterGrade) VALUES
('GR001','REG001',8.0,8.5,8.3,'B+'),
('GR002','REG002',9.0,9.2,9.1,'A'),
('GR003','REG003',7.0,8.0,7.6,'B');

INSERT INTO Users (UserID, Username, Password, Role, Status) VALUES
('U001','SV001','123456','Student','Active'),
('U002','SV002','123456','Student','Active'),
('U003','SV003','123456','Student','Active'),
('U004','SV004','123456','Student','Locked'),
('U005','GV001','123456','Lecturer','Active'),
('U006','GV002','123456','Lecturer','Active'),
('U007','GV003','123456','Lecturer','Active'),
('U008','admin','admin123','Administrator','Active');
