<?php
// src/App/Form/LanguageTaskType.php

namespace App\Form;

use App\Entity\eFaInitTask;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\ChoiceType;

class LanguageEditTaskType extends AbstractType
{
    public function buildForm(FormBuilderInterface $builder, array $options): void
    {
        $builder
            ->add('Language', ChoiceType::class, array(
                'choices' => array(
                    'Czech' => 'cz',
                    'Danish' => 'da',
                    'Dutch' => 'nl',
                    'English' => 'en',
                    'French' => 'fr',
                    'German' => 'de',
                    'Greek' => 'el',
                    'Italian' => 'it',
                    'Norwegian' => 'no',
                    'Portuguese' => 'pt_PT',
                    'Russian' => 'ru',
                    'Simplified Chinese' => 'zh_CN',
                    'Swedish' => 'sv',
                    'Traditional Chinese' => 'zh_TW',
                    'Turkish' => 'tr',
                    ),
                'preferred_choices' => array($options['locale']),
                'expanded' => false,
                'multiple' => false,
                'attr' => array('onchange' => "window.location.replace('../' + this.value + '/edit')"),
                'choice_translation_domain' => true
                ))
            ->add('Save', SubmitType::class)
        ;
    }
    public function configureOptions(OptionsResolver $resolver): void
    {
        $resolver->setDefaults(array(
            'data_class' => eFaInitTask::class,
            'csrf_token_id' => 'language_task'
        ));
        $resolver->setRequired('locale');
    }
}
?>
