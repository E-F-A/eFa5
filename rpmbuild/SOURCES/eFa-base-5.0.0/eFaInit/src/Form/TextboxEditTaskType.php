<?php
// src/App/Form/TextboxTaskType.php

namespace App\Form;

use App\Entity\eFaInitTask;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TextType;

class TextboxEditTaskType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('Textbox', TextType::class, array(
                'label'             => $options['varLabel'],
                'required'          => false,
                'trim'              => true,
                'property_path'     => $options['varProperty'],
                'data'              => $options['varData'],
            ))
            ->add('Save', SubmitType::class, array(
                'validation_groups' => array($options['varProperty']),
            ))
            ;
    }
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(array(
            'data_class'    => eFaInitTask::class,
            'csrf_token_id' => 'eFaInit'
        ));
        $resolver->setRequired('varLabel');
        $resolver->setRequired('varProperty');
        $resolver->setRequired('varData');
    }
}
?>
