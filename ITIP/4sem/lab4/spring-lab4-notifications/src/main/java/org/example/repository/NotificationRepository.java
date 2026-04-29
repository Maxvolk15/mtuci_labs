package org.example.repository;
import java.util.List;

import org.example.model.entity.Notification;
import org.example.model.enums.NotificationChannel;
import org.example.model.enums.NotificationStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {
    List<Notification> findByStatus(NotificationStatus status);
    List<Notification> findByChannel(NotificationChannel channel);
    List<Notification> findByRecipientId(Long recipientId);
    List<Notification> findByStatusAndChannel(NotificationStatus status, NotificationChannel channel);
    List<Notification> findByStatusOrderByCreatedAtDesc(NotificationStatus status);
    
    @Query("""
    select n
    from Notification n
    where n.status = :status
    and n.channel = :channel
    """)
    List<Notification> findByStatusAndChannelCustom(@Param("status") NotificationStatus status, @Param("channel") NotificationChannel channel);
    
    @Query(value = """
    select *
    from notifications
    where status = :status
    and channel = :channel
    """, nativeQuery = true)
    List<Notification> findNativeByStatusAndChannel(@Param("status") String status, @Param("channel") String channel);

    @Query("""
        select n 
        from Notification n 
        where n.recipient.id = :recipientId 
        and n.status = :status
    """)
    List<Notification> findByRecipientIdAndStatusCustom(@Param("recipientId") Long recipientId, @Param("status") NotificationStatus status);
}