# Part 1: Application Selection & Analysis

## Application: Microsoft Teams

### Purpose

Microsoft Teams is a communication and collaboration application designed to help people work together from different locations. It combines messaging, video meetings, voice calls, file sharing, and collaboration tools in one platform. It is commonly used by companies, schools, universities, and other organizations to communicate and organize their work. Instead of using separate applications for chat, meetings, and document collaboration, users can access these functions from Teams.

### Target Users

The main users of Microsoft Teams are employees, students, teachers, managers, and organizations that need to communicate and collaborate online. Companies can use Teams for internal communication, project meetings, file sharing, and remote work. Schools and universities can use it for online classes, group projects, meetings, and communication between teachers and students. It can also be used to communicate with people outside an organization through guest access or meeting invitations.

### Key Features

1. **Chat and messaging:** Users can send private messages, participate in group chats, react to messages, and share information in real time.
2. **Video and audio meetings:** Users can create or join online meetings with video, audio, and meeting controls.
3. **Screen sharing:** Participants can share their entire screen or specific content during a meeting.
4. **File sharing and collaboration:** Users can upload, share, access, and collaborate on documents.
5. **Teams and channels:** Organizations can create teams and channels to separate communication by department, class, project, or topic.
6. **Notifications:** Users receive notifications for new messages, mentions, calls, meetings, and other important activity.
7. **Calendar and meeting scheduling:** Users can schedule meetings, invite participants, and manage upcoming meetings.
8. **Microsoft 365 integration:** Teams integrates with services such as OneDrive, SharePoint, Word, Excel, and PowerPoint.

### Technology Stack

Microsoft Teams is a cloud-based application available as a desktop, web, and mobile application. The current desktop client uses Microsoft Edge WebView2 for its user interface. Teams also integrates with Microsoft 365 services and technologies such as Microsoft Graph, Microsoft 365 Groups, SharePoint, and OneDrive. Because Microsoft does not publicly expose every internal technology used by the platform, this analysis focuses only on publicly documented components.

### Critical Functions

The most critical functions are user authentication, chat and message delivery, joining and maintaining audio/video meetings, meeting scheduling, and file access and sharing. These functions are essential because they directly support communication and collaboration. A failure in authentication could prevent users from accessing Teams, while failures in chat or meetings could interrupt work or classes. File permissions are also critical because users must be able to access authorized documents without exposing information to unauthorized people. For this reason, these areas should receive the highest testing priority.
