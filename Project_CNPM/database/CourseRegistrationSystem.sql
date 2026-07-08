CREATE DATABASE CourseRegistrationSystem;
GO

USE CourseRegistrationSystem;
GO

DROP TABLE Users; --9
DROP TABLE Student; --5
DROP TABLE CourseClass; --4
DROP TABLE Lecturer; --6
DROP TABLE Admin; --3
DROP TABLE Subject; --8
DROP TABLE Subject_Prerequisite; --2
DROP TABLE Registration; --1
DROP TABLE RegistrationPeriod; --7



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
    room VARCHAR(50),
    dayOfWeek VARCHAR(10),
    startTime TIME,
    endTime TIME,
    maxCapacity INT,
    status VARCHAR(20),
    FOREIGN KEY(subjectID) REFERENCES Subject(subjectID),
    FOREIGN KEY(lecturerID) REFERENCES Lecturer(lecturerID),
);

CREATE TABLE PeriodClass
(
    periodID VARCHAR(20),
    classID VARCHAR(20),
    currentEnrolled INT DEFAULT 0,
    status VARCHAR(20) CHECK (status IN ('Upcoming','Open','Closed')),
    PRIMARY KEY(periodID,classID),
    FOREIGN KEY(periodID)
        REFERENCES RegistrationPeriod(periodID),
    FOREIGN KEY(classID)
        REFERENCES CourseClass(classID)
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




INSERT INTO Student(studentID, fullName, dateOfBirth, email, password, major, earnedCredits, status) VALUES
('SV001','Nguyen Van An','2004-05-12','an@gmail.com','123456','Information Technology',45,'Active'),
('SV002','Tran Thi Binh','2004-09-20','binh@gmail.com','123456','Computer Science',60,'Active'),
('SV003','Le Minh Chau','2005-01-15','chau@gmail.com','123456','Software Engineering',20,'Active'),
('SV004','Pham Quoc Dat','2004-11-10','dat@gmail.com','123456','Information Systems',80,'Locked'),
('SV005','Nguyen Minh Hoang','2004-03-21','hoangnm@gmail.com','123456','Information Technology',35,'Active'),
('SV006','Tran Khanh Linh','2004-12-11','linhtk@gmail.com','123456','Computer Science',50,'Active'),
('SV007','Le Gia Huy','2003-10-05','huylg@gmail.com','123456','Software Engineering',75,'Active'),
('SV008','Pham Ngoc Mai','2005-02-16','maipn@gmail.com','123456','Information Systems',18,'Active'),
('SV009','Do Minh Quan','2004-06-25','quandm@gmail.com','123456','Artificial Intelligence',42,'Active'),
('SV010','Vo Nhat Anh','2004-09-09','anhvn@gmail.com','123456','Cyber Security',65,'Active'),
('SV011','Bui Hai Yen','2005-01-30','yenbh@gmail.com','123456','Computer Science',15,'Active'),
('SV012','Hoang Duc Long','2004-08-17','longhd@gmail.com','123456','Information Technology',55,'Active');

INSERT INTO Lecturer (lecturerID, fullName, email, password, department, title, status) VALUES
('GV001','Nguyen Van Cuong','nva@university.edu','123456','Information Technology','Professor','Active'),
('GV002','Tran Thi Bich','ttb@university.edu','123456','Computer Science','Associate Professor','Active'),
('GV003','Le Van Huy','lvc@university.edu','123456','Software Engineering','Lecturer','Active'),
('GV004','Nguyen Hoang Minh','nhminh@university.edu','123456','Information Technology','Lecturer','Active'),
('GV005','Tran Thi Thu Ha','ttha@university.edu','123456','Computer Science','Senior Lecturer','Active'),
('GV006','Le Quoc Huy','lqhuy@university.edu','123456','Software Engineering','Professor','Active'),
('GV007','Pham Minh Tuan','pmtuan@university.edu','123456','Artificial Intelligence','Associate Professor','Active'),
('GV008','Do Thanh Phuong','dtphuong@university.edu','123456','Cyber Security','Lecturer','Active');

INSERT INTO Admin (adminID, username, password, fullName, email, status) VALUES
('AD001','admin','admin123','System Administrator','admin@university.edu','Active');

INSERT INTO Subject (subjectID, subjectName, credits, tuition, department, description, status) VALUES
('SUB001','Programming Fundamentals',3,4500000,'IT','Basic programming','Active'),
('SUB002','Object-Oriented Programming',3,4500000,'IT','OOP with Python','Active'),
('SUB003','Database Systems',3,4500000,'IT','SQL Server Database','Active'),
('SUB004','Data Structures and Algorithms',4,6000000,'IT','DSA','Active'),
('SUB005','Computer Networks',3,4500000,'IT','Networking Fundamentals','Active'),
('SUB006','Operating Systems',3,4500000,'IT','Operating System Concepts','Active'),
('SUB007','Software Testing',3,4500000,'SE','Software Testing','Active'),
('SUB008','Artificial Intelligence',3,5000000,'AI','Introduction to AI','Active'),
('SUB009','Machine Learning',4,6500000,'AI','Machine Learning Basics','Active'),
('SUB010','Web Development',3,4500000,'IT','HTML CSS JavaScript','Active'),
('SUB011','Mobile Application Development',3,5000000,'IT','Android Programming','Active'),
('SUB012','Cloud Computing',3,5000000,'IT','AWS Cloud','Active'),
('SUB013','Information Security',3,5000000,'IT','Network Security','Active');

INSERT INTO Subject_Prerequisite (subjectID, prerequisiteID) VALUES
('SUB002','SUB001'),
('SUB004','SUB002'),
('SUB003','SUB001'),
('SUB006','SUB001'),
('SUB007','SUB002'),
('SUB008','SUB004');

INSERT INTO RegistrationPeriod (periodID, semesterName, startDate, endDate, regOpenDate, regCloseDate, status) VALUES
('P001', 'Semester 1 - 2026', '2026-09-01', '2026-12-31', '2026-08-01 08:00', '2026-08-15 17:00', 'Open'),
('P002','Semester 2 - 2026','2027-01-10','2027-05-15','2026-12-15 08:00','2026-12-30 17:00','Open'),
('P003','Summer 2027','2027-06-01','2027-08-15','2027-05-01 08:00','2027-05-15 17:00','Closed'),
('P004','Semester 1 - 2027','2027-09-01','2027-12-31','2027-08-01 08:00','2027-08-15 17:00','Open'),
('P005','Semester 2 - 2027','2028-01-10','2028-05-15','2027-12-15 08:00','2027-12-30 17:00','Upcoming'),
('P006','Summer 2028','2028-06-01','2028-08-15','2028-05-01 08:00','2028-05-15 17:00','Upcoming');

INSERT INTO CourseClass(classID, subjectID, lecturerID, room, dayOfWeek, startTime, endTime, maxCapacity, status) VALUES
('CLS001','SUB001','GV001','A101','Monday','06:45','09:15',50,'Open'),
('CLS002','SUB002','GV002','B201','Tuesday','09:25','11:55',40,'Open'),
('CLS003','SUB003','GV003','C301','Wednesday','12:10','14:40',35,'Close'),
('CLS004','SUB004','GV001','A202','Thursday','14:50','17:20',30,'Upcoming'),
('CLS005','SUB005','GV002','B202','Friday','17:30','20:00',40,'Close'),
('CLS006','SUB006','GV004','D101','Monday','09:25','11:55',45,'Open'),
('CLS007','SUB007','GV001','D201','Tuesday','12:10','14:40',35,'Open'),
('CLS008','SUB008','GV002','AI101','Wednesday','14:50','17:20',30,'Open'),
('CLS009','SUB009','GV007','AI102','Thursday','17:30','20:00',30,'Upcoming'),
('CLS010','SUB010','GV004','LAB01','Friday','06:45','09:15',40,'Close'),
('CLS011','SUB011','GV005','LAB02','Monday','12:10','14:40',35,'Open'),
('CLS012','SUB012','GV001','Cloud01','Tuesday','14:50','17:20',40,'Open'),
('CLS013','SUB013','GV008','Sec101','Wednesday','17:30','20:00',35,'Open'),
('CLS014','SUB003','GV003','C302','Thursday','09:25','11:55',40,'Open');

INSERT INTO PeriodClass(periodID, classID, currentEnrolled, status) VALUES
('P001','CLS001',5,'Open'),
('P001','CLS002',6,'Open'),
('P001','CLS003',0,'Closed'),
('P002','CLS001',0,'Upcoming');

INSERT INTO Registration (regID, studentID, classID, periodID, status) VALUES
('REG001','SV001','CLS001','P001','Approved'),
('REG002','SV001','CLS003','P001','Approved'),
('REG003','SV002','CLS001','P001','Approved'),
('REG004','SV003','CLS002','P001','Pending'),
('REG005','SV004','CLS005','P001','Approved'),
('REG006','SV005','CLS006','P001','Approved'),
('REG007','SV006','CLS007','P001','Approved'),
('REG008','SV007','CLS008','P001','Pending'),
('REG009','SV008','CLS009','P001','Approved'),
('REG010','SV009','CLS010','P001','Approved'),
('REG011','SV010','CLS011','P001','Approved'),
('REG012','SV011','CLS012','P001','Pending'),
('REG013','SV012','CLS013','P001','Approved'),
('REG014','SV005','CLS005','P001','Approved');


INSERT INTO Users (UserID, Username, Password, Role, Status) VALUES
('U001','SV001','123456','Student','Active'),
('U002','SV002','123456','Student','Active'),
('U003','SV003','123456','Student','Active'),
('U004','SV004','123456','Student','Locked'),
('U005','GV001','123456','Lecturer','Active'),
('U006','GV002','123456','Lecturer','Active'),
('U007','GV003','123456','Lecturer','Active'),
('U008','admin','admin123','Admin','Active'),
('U009','SV005','123456','Student','Active'),
('U010','SV006','123456','Student','Active'),
('U011','SV007','123456','Student','Active'),
('U012','SV008','123456','Student','Active'),
('U013','SV009','123456','Student','Active'),
('U014','SV010','123456','Student','Active'),
('U015','SV011','123456','Student','Active'),
('U016','SV012','123456','Student','Active'),
('U017','GV004','123456','Lecturer','Active'),
('U018','GV005','123456','Lecturer','Active'),
('U019','GV006','123456','Lecturer','Active'),
('U020','GV007','123456','Lecturer','Active'),
('U021','GV008','123456','Lecturer','Active');